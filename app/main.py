import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from api.routes import router
from contextlib import asynccontextmanager
from mcp_tools.connection import connection
from config import FASTAPI_HOST, FASTAPI_PORT
from fastapi.middleware.cors import CORSMiddleware
from utils.error_handler import global_exception_handler
from utils.logger import logger
from utils.middleware import LoggingMiddleware
from auth.auth import router as auth_router
from admin.dashboard import router as dashboard_router
from admin.analytics import router as analytics_router
from pathlib import Path


@asynccontextmanager
async def lifespan(app: FastAPI):
    mcp_connected = False
    try:
        await connection.connect()
        mcp_connected = True
    except Exception:
        # MCP tools are optional for the HTTP API. Keep the API available
        # while the MCP subprocess is unavailable or being restarted.
        logger.exception("MCP server connection failed; continuing without MCP tools.")

    try:
        yield
    finally:
        if mcp_connected:
            await connection.disconnect()


app = FastAPI(
    title="Enterprise AI Chatbot API",
    description="GraphRAG + MCP + Ollama + Neo4j + ChromaDB",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(
    analytics_router,
    prefix="/admin",
    tags=["Analytics"]
)

app.include_router(
    dashboard_router,
    prefix="/admin",
    tags=["Dashboard"]
)

app.add_exception_handler(
    Exception,
    global_exception_handler
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    LoggingMiddleware
)
# Include API routers
app.include_router(router)
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)


@app.get("/chat-ui", include_in_schema=False)
def chatbot_interface():
    """Serve the bundled chatbot interface from the same origin as the API."""
    frontend_file = Path(__file__).resolve().parents[1] / "frontend" / "index.html"
    return FileResponse(frontend_file)

@app.get("/")
def root():
    """Root endpoint returning API information."""
    return {
        "name": "Enterprise AI Chatbot API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=FASTAPI_HOST or "127.0.0.1",
        port=FASTAPI_PORT or 8000,
        reload=True,
    )
