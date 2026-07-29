from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from auth.dependencies import get_current_user
from llm.provider import generate_response
from logs.logger import logger

router = APIRouter(
    tags=["Chat"],
)


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        examples=["What is Artificial Intelligence?"],
    )


class ChatResponse(BaseModel):
    response: str


def hybrid_chat(message: str) -> str:
    """Load the hybrid pipeline only when a chat request needs it."""
    from hybrid.pipeline import hybrid_chat as run_hybrid_chat

    return run_hybrid_chat(message)


@router.post(
    "/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
)
def chat(
    request: ChatRequest,
    current_user: str = Depends(get_current_user),
):
    """
    Send a message to the Enterprise AI Chatbot.
    """

    try:
        logger.info("User question received: %s", request.message)

        answer = hybrid_chat(request.message)

        if not answer:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="The language model returned an empty response",
            )

        logger.info("Chat response generated successfully")

        return ChatResponse(
            response=answer,
        )

    except HTTPException:
        raise

    except Exception as exc:
        logger.exception("Chat endpoint failed")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to generate chatbot response",
        ) from exc
