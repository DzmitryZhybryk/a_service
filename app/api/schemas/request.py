"""Module for storage pydantic models"""

from email_validator import validate_email
from pydantic import validator

from app.api.schemas.base import UserBase


class RegistrateUser(UserBase):
    password: str
    confirm_password: str

    @validator("confirm_password")
    def passwords_match(cls, confirm_password: str, values: dict) -> str:
        if "password" in values and confirm_password != values["password"]:
            raise ValueError("Password mismatch!")

        return confirm_password

    @validator("email")
    def validate_email(cls, email: str) -> str:
        validate_email(email)
        return email

    class Config:
        schema_extra = {
            "example": {
                "username": "admin",
                "password": "somedificultpassword",
                "confirm_password": "somedificultpassword",
                "nickname": "BigDaddy",
                "email": "mr.jibrik@mail.ru",
                "first_name": "Jon",
                "last_name": "Smith",
                "birthday": "2023-06-08",
                "user_role": "base_user"
            }
        }
