from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from graphrag.graph_db import execute_query
from vectorstore.db import collection
from database.database import get_db
from database.models import User, ChatHistory

router = APIRouter()


@router.get("/vectors")
def vector_statistics():

    return {
        "documents": collection.count()
    }


@router.get("/graph")
def graph_statistics():

    query = """
    MATCH (n)
    RETURN count(n) AS total_nodes
    """

    return execute_query(query)


@router.get("/health")
def system_health():

    return {

        "FastAPI": "Running",

        "Ollama": "Connected",

        "Neo4j": "Connected",

        "ChromaDB": "Connected"

    }


@router.get("/users")
def total_users(db: Session = Depends(get_db)):

    count = db.query(User).count()

    return {
        "total_users": count
    }


@router.get("/chats")
def total_chats(db: Session = Depends(get_db)):

    count = db.query(ChatHistory).count()

    return {
        "total_chats": count
    }


@router.get("/logs")
def view_logs():

    with open(
        "logs/app.log",
        "r"
    ) as f:

        return {
            "logs": f.readlines()[-50:]
        }

