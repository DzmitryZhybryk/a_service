import asyncio
from argparse import ArgumentParser

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from hypercorn.asyncio import serve
from hypercorn.config import Config

from app.api.routes import router as auth_router
from app.database.models import Role, User
from app.database.postgres import engine
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
    role, user = Role(), User()
    await role.create_init_roles()
    await user.creat_init_user()

    """
    Use this if you want create init database table without alembic
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    """


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await engine.dispose()


def main() -> None:
    args = parser.parse_args()
    config = Config()
    config.bind = [f"{args.host}:{args.port}"]
    asyncio.run(serve(app, config))  # type: ignore


if __name__ == '__main__':
    main()
