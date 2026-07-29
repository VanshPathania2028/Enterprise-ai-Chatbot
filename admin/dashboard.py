from fastapi import APIRouter
from fastapi import Depends

from auth.dependencies import get_current_user
router = APIRouter()


@router.get("/dashboard")
def dashboard():

    return {
        "project": "Enterprise AI Chatbot",
        "status": "Running",
        "version": "1.0.0"
    }
@router.get("/users")
def total_users(
    current_user: str = Depends(get_current_user)
):

    return {
        "total_users": 152
    }