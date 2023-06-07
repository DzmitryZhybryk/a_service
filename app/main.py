import asyncio
from argparse import ArgumentParser

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from hypercorn.asyncio import serve
from hypercorn.config import Config

from app.api.routes import router as auth_router
from app.api.services import AuthenticationStorage
from app.database.db import engine
from app.database.db import use_session
from app.utils.funcs import get_app_metadata

app_metadata = asyncio.run(get_app_metadata())

parser = ArgumentParser()

parser.add_argument("--host", help=f"IPv4/IPv6 address API server would listen on", default="0.0.0.0")

parser.add_argument("--port", help=f"TCP port API server would listen on", type=int, default=8001)

app = FastAPI(docs_url="/api/v1/docs", redoc_url="/api/v1/redoc", title=app_metadata.name, version=app_metadata.version,
              description=app_metadata.description, swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router, prefix="/api/v1")


@app.on_event("startup")
async def on_startup() -> None:
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    async for session in use_session():
        authentication_storage_handle = AuthenticationStorage(session=session)
        await authentication_storage_handle.create_init_database_data()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await engine.dispose()


# @app.exception_handler(RequestValidationError)
# def validation_exception_handler(request: Request, exc: RequestValidationError):
#     """Кастомное исключение для вывода более информативного ответа 422 ошибки"""
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
#     )


# @app.middleware('http')
# async def log_exception(request: Request, call_next):
#     """Функция для логирования необработанных ошибок"""
#     try:
#         return await call_next(request)
#     except Exception as err:
#         if logging.sentry_activate:
#             sentry_sdk.capture_exception(error=err)
#         raise err


def main() -> None:
    args = parser.parse_args()
    config = Config()
    config.bind = [f"{args.host}:{args.port}"]
    asyncio.run(serve(app, config))  # type: ignore


if __name__ == '__main__':
    main()
