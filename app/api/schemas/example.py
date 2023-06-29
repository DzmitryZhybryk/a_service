base_responses = {
    403: {
        "description": "Not enough privileges",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Invalid API key"
                }
            }
        }
    },
    404: {
        "description": "Resource not found",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Resource not found"
                }
            }
        }
    }
}

conflict: dict = {409: {
    "description": "Resource already exist",
    "content": {
        "application/json": {
            "example": {
                "detail": "The same data already exist in database"
            }
        }
    }
}}

get_user_response: dict = {200: {
    "description": "Successful Response",
    "content": {
        "application/json": {
            "example": {
                "id": 1,
                "username": "admin",
                "nickname": "BigDaddy",
                "email": "my_email@gmail.com",
                "first_name": "Jon",
                "last_name": "Smith",
                "birthday": "2023-06-08",
                "is_user_activate": True,
                "main_photo": "/some/photo/url",
                "role": {
                    "id": 1,
                    "role": "base_user"
                }
            }
        }
    }
}} | base_responses

registrate_response: dict = {201: {
    "description": "Successful Response",
    "content": {
        "application/json": {
            "example": {
                "confirm_registration_key": "string",
                "username": "string",
                "email": "string"
            }
        }
    }
}} | base_responses | conflict
