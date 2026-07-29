from fastapi import HTTPException


def require_admin(role):

    if role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin privileges required."
        )