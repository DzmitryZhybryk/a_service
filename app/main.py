import asyncio
from argparse import ArgumentParser

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from hypercorn.asyncio import serve
from hypercorn.config import Config

from app.dependencies import AuthenticationStorage
from app.routes import router as auth_router

authentication_storage_handle = AuthenticationStorage()
app_metadata = asyncio.run(authentication_storage_handle.get_app_metadata())

parser = ArgumentParser()

parser.add_argument("--host", help=f"Application host", type=str, default="0.0.0.0")

parser.add_argument("--port", help=f"Application port", type=str, default=8001)

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


# @app.on_event("startup")
# async def on_startup() -> None:
# if logging.sentry_activate:
#     sentry_sdk.init(
#         dsn="https://65de844898564b009441a526b7877f44@o4504518318292992.ingest.sentry.io/4504518327533568",
#         traces_sample_rate=1,
#     )

# logger.info(f"Начало работы {APP_NAME}")
# metadata.create_all(engine)
# logger.info("Создание таблиц в базе данных")
#
# await database.connect()
# logger.info("Установлено соединение с базой данных")
# init_data = UserHandlers()
# await init_data.create_init_data()
# logger.info("Создание init данных в базе данных")


# @app.on_event("shutdown")
# async def on_shutdown() -> None:
#     await database.disconnect()
#     logger.info(f"{APP_NAME} остановлен")


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
