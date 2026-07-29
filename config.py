import os

from dotenv import load_dotenv

ENV = os.getenv("ENV", "development")

if ENV == "production":
    load_dotenv(".env.production")
else:
    load_dotenv(".env")


OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434",
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2",
)

STOCK_API_KEY = os.getenv("STOCK_API_KEY")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")



NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")



CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH")


FASTAPI_HOST = os.getenv("FASTAPI_HOST", "127.0.0.1")

FASTAPI_PORT = int(
    os.getenv("FASTAPI_PORT", 8000)
)



SECRET_KEY = os.getenv("SECRET_KEY")

JWT_ALGORITHM = os.getenv(
    "JWT_ALGORITHM",
    "HS256"
)

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        60
    )
)


LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)
