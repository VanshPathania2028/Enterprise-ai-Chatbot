import json
from pathlib import Path

from fastapi import APIRouter, HTTPException

from auth.models import (
    UserRegister,
    UserLogin
)

from auth.security import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter()


DATABASE = Path("users/users.json")


def load_users():
    DATABASE.parent.mkdir(parents=True, exist_ok=True)
    if not DATABASE.exists():
        DATABASE.write_text("[]", encoding="utf-8")

    with DATABASE.open("r", encoding="utf-8") as file:
        return json.load(file)


@router.post("/register")

def register(user: UserRegister):

    users = load_users()

    for u in users:
        if u["username"] == user.username:
            raise HTTPException(
                400,
                "User already exists"
            )

    users.append(
        {
            "username": user.username,
            "password": hash_password(
                user.password
            )
        }
    )

    with DATABASE.open("w", encoding="utf-8") as f:
        json.dump(
            users,
            f,
            indent=4
        )

    return {
        "message": "Registration Successful"
    }


@router.post("/login")

def login(user: UserLogin):

    users = load_users()

    for u in users:

        if (
            u["username"] == user.username
            and verify_password(
                user.password,
                u["password"]
            )
        ):

            token = create_access_token(
                {
                    "sub": user.username
                }
            )

            return {
                "access_token": token,
                "token_type": "bearer"
            }

    raise HTTPException(
        401,
        "Invalid Username or Password"
    )
