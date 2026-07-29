from contextlib import asynccontextmanager
from pathlib import Path
from uuid import uuid4
import logging

import requests

from fastapi import (
    FastAPI,
    File,
    Depends,
    HTTPException,
    Request,
    UploadFile,
    status,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from config import (
    FASTAPI_HOST,
    FASTAPI_PORT,
    OLLAMA_MODEL,
)

from rag.rag_chat import rag_chat
from rag.ingest import (
    delete_document_from_vectorstore,
    ingest_pdf,
)
from tools.live_data import (
    get_stock_quote,
    get_weather,
    live_chat_response,
)
from auth.auth import router as auth_router
from auth.dependencies import get_current_user


logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s - %(name)s - "
        "%(levelname)s - %(message)s"
    ),
)

logger = logging.getLogger(
    "enterprise-ai-chatbot"
)


UPLOAD_DIRECTORY = Path(
    "documents/uploads"
)

UPLOAD_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)

MAXIMUM_FILE_SIZE = (
    10 * 1024 * 1024
)


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        examples=[
            "What is artificial intelligence?"
        ],
    )

class SourceResponse(BaseModel):
    filename: str
    chunk: int | None = None


class ChatResponse(BaseModel):
    response: str
    status: str = "success"
    sources: list[SourceResponse] = []


class HealthResponse(BaseModel):
    status: str
    service: str
    model: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(
        "Enterprise AI Chatbot is starting"
    )

    yield

    logger.info(
        "Enterprise AI Chatbot is shutting down"
    )


app = FastAPI(
    title="Enterprise AI Chatbot",
    description=(
        "Enterprise chatbot using Ollama, "
        "RAG, GraphRAG, LangGraph, "
        "LlamaIndex and MCP."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    # Vite uses 5173 by default but selects another local port when that one
    # is occupied. Permit local development servers without opening CORS to
    # arbitrary remote origins.
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])


@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    logger.exception(
        "Unhandled error on %s %s",
        request.method,
        request.url.path,
    )

    return JSONResponse(
        status_code=(
            status.HTTP_500_INTERNAL_SERVER_ERROR
        ),
        content={
            "status": "error",
            "detail": (
                "An internal server error occurred."
            ),
        },
    )


@app.get("/")
def root():
    return {
        "status": "success",
        "message": (
            "Enterprise AI Chatbot API "
            "is running."
        ),
        "docs": "/docs",
    }


@app.get(
    "/health",
    response_model=HealthResponse,
)
def health_check():
    return HealthResponse(
        status="healthy",
        service="Enterprise AI Chatbot",
        model=OLLAMA_MODEL,
    )


@app.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(request: ChatRequest, _: str = Depends(get_current_user)):
    user_message = (
        request.message.strip()
    )

    if not user_message:
        raise HTTPException(
            status_code=(
                status.HTTP_400_BAD_REQUEST
            ),
            detail="Message cannot be empty.",
        )

    try:
        logger.info(
            "Chat request received: %s",
            user_message[:100],
        )

        try:
            live_response = live_chat_response(user_message)
        except (LookupError, RuntimeError, ValueError) as error:
            return ChatResponse(response=str(error))
        except requests.RequestException:
            return ChatResponse(
                response="The live-data service is unavailable. Please try again shortly."
            )

        if live_response is not None:
            return ChatResponse(response=live_response)

        result = rag_chat(user_message)

        if isinstance(result, dict):
            answer = result.get("answer") or result.get("response")
            sources = result.get("sources", [])
        else:
            answer = result
            sources = []

        if not answer:
            raise HTTPException(
                status_code=(
                    status.HTTP_500_INTERNAL_SERVER_ERROR
                ),
                detail=(
                    "The chatbot generated "
                    "an empty response."
                ),
            )

        return ChatResponse(
            response=str(answer),
            status="success",
            sources=sources,
        )

    except HTTPException:
        raise

    except Exception as error:
        logger.exception(
            "Chat processing failed"
        )

        raise HTTPException(
            status_code=(
                status.HTTP_500_INTERNAL_SERVER_ERROR
            ),
            detail=(
                "Chat processing failed: "
                f"{str(error)}"
            ),
        ) from error


@app.get("/tools/weather")
def weather(city: str, _: str = Depends(get_current_user)):
    """Get current weather for a city from Open-Meteo."""
    try:
        return get_weather(city)
    except (LookupError, ValueError) as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error
    except requests.RequestException as error:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Weather service is unavailable.") from error


@app.get("/tools/stock")
def stock(symbol: str, _: str = Depends(get_current_user)):
    """Get a latest available stock quote from Alpha Vantage."""
    try:
        return get_stock_quote(symbol)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error
    except (LookupError, RuntimeError) as error:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(error)) from error
    except requests.RequestException as error:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Stock service is unavailable.") from error


@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    _: str = Depends(get_current_user),
):
    if not file.filename:
        raise HTTPException(
            status_code=(
                status.HTTP_400_BAD_REQUEST
            ),
            detail=(
                "The uploaded file "
                "has no filename."
            ),
        )

    original_name = Path(
        file.filename
    ).name

    if not original_name.lower().endswith(
        ".pdf"
    ):
        raise HTTPException(
            status_code=(
                status.HTTP_400_BAD_REQUEST
            ),
            detail=(
                "Only PDF files are allowed."
            ),
        )

    allowed_content_types = {
        "application/pdf",
        "application/octet-stream",
    }

    if (
        file.content_type
        and file.content_type
        not in allowed_content_types
    ):
        raise HTTPException(
            status_code=(
                status.HTTP_400_BAD_REQUEST
            ),
            detail=(
                "Only PDF files are allowed."
            ),
        )

    unique_name = (
        f"{uuid4()}_{original_name}"
    )

    file_path = (
        UPLOAD_DIRECTORY / unique_name
    )

    try:
        file_content = await file.read()

        if not file_content:
            raise HTTPException(
                status_code=(
                    status.HTTP_400_BAD_REQUEST
                ),
                detail=(
                    "The uploaded PDF is empty."
                ),
            )

        if (
            len(file_content)
            > MAXIMUM_FILE_SIZE
        ):
            raise HTTPException(
                status_code=(
                    status.HTTP_400_BAD_REQUEST
                ),
                detail=(
                    "The PDF must be "
                    "smaller than 10 MB."
                ),
            )

        if not file_content.startswith(
            b"%PDF"
        ):
            raise HTTPException(
                status_code=(
                    status.HTTP_400_BAD_REQUEST
                ),
                detail=(
                    "The uploaded file "
                    "is not a valid PDF."
                ),
            )

        file_path.write_bytes(
            file_content
        )

        logger.info(
            "PDF saved successfully: %s",
            file_path,
        )

        ingestion_result = ingest_pdf(
            str(file_path)
        )

        return {
            "status": "success",
            "message": (
                "Document uploaded and "
                "indexed successfully."
            ),
            "filename": original_name,
            "saved_filename": unique_name,
            "saved_path": str(file_path),
            "size_bytes": len(
                file_content
            ),
            "chunks_added": (
                ingestion_result.get(
                    "chunks_added",
                    0,
                )
            ),
        }

    except HTTPException:
        if file_path.exists():
            file_path.unlink()

        raise

    except Exception as error:
        logger.exception(
            "PDF upload failed"
        )

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=(
                status.HTTP_500_INTERNAL_SERVER_ERROR
            ),
            detail=(
                "Document upload failed: "
                f"{str(error)}"
            ),
        ) from error

    finally:
        await file.close()


@app.get("/documents")
def list_documents(_: str = Depends(get_current_user)):
    documents = []

    for file_path in (
        UPLOAD_DIRECTORY.glob("*.pdf")
    ):
        stored_name = file_path.name

        if "_" in stored_name:
            original_name = (
                stored_name.split(
                    "_",
                    1,
                )[1]
            )
        else:
            original_name = stored_name

        file_information = (
            file_path.stat()
        )

        documents.append(
            {
                "original_filename": (
                    original_name
                ),
                "saved_filename": (
                    stored_name
                ),
                "size_bytes": (
                    file_information.st_size
                ),
                "uploaded_at": (
                    file_information.st_mtime
                ),
            }
        )

    documents.sort(
        key=lambda document: (
            document["uploaded_at"]
        ),
        reverse=True,
    )

    return {
        "status": "success",
        "count": len(documents),
        "documents": documents,
    }


@app.delete(
    "/documents/{filename}"
)
def remove_document(
    filename: str,
    _: str = Depends(get_current_user),
):
    safe_filename = Path(
        filename
    ).name

    file_path = (
        UPLOAD_DIRECTORY
        / safe_filename
    )

    if not file_path.exists():
        matching_files = [
            candidate
            for candidate in UPLOAD_DIRECTORY.glob("*.pdf")
            if candidate.name.split("_", 1)[-1]
            == safe_filename
        ]

        if len(matching_files) == 1:
            file_path = matching_files[0]
            safe_filename = file_path.name
        elif len(matching_files) > 1:
            raise HTTPException(
                status_code=(
                    status.HTTP_409_CONFLICT
                ),
                detail=(
                    "More than one document has this "
                    "original filename. Use its saved filename."
                ),
            )
        else:
            raise HTTPException(
                status_code=(
                    status.HTTP_404_NOT_FOUND
                ),
                detail="Document not found.",
            )

    if not file_path.is_file():
        raise HTTPException(
            status_code=(
                status.HTTP_400_BAD_REQUEST
            ),
            detail=(
                "Invalid document path."
            ),
        )

    if (
        file_path.suffix.lower()
        != ".pdf"
    ):
        raise HTTPException(
            status_code=(
                status.HTTP_400_BAD_REQUEST
            ),
            detail="Invalid document.",
        )

    try:
        deletion_result = (
            delete_document_from_vectorstore(
                safe_filename
            )
        )

        file_path.unlink()

        logger.info(
            "Document deleted: %s",
            safe_filename,
        )

        return {
            "status": "success",
            "message": (
                "Document and vector data "
                "deleted successfully."
            ),
            "filename": safe_filename,
            "chunks_deleted": (
                deletion_result.get(
                    "chunks_deleted",
                    0,
                )
            ),
        }

    except Exception as error:
        logger.exception(
            "Document deletion failed"
        )

        raise HTTPException(
            status_code=(
                status.HTTP_500_INTERNAL_SERVER_ERROR
            ),
            detail=(
                "Unable to delete document: "
                f"{str(error)}"
            ),
        ) from error


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=FASTAPI_HOST,
        port=FASTAPI_PORT,
        reload=True,
    )
