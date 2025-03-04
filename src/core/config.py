import pathlib
from contextlib import asynccontextmanager

from pydantic_settings import BaseSettings
from importlib import import_module
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase


DATABASE_URL = "postgresql+asyncpg://postgres:moggerisme@localhost/task_manager_db"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


@asynccontextmanager
async def get_db():
    async with async_session() as session:
        yield session


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



class Settings(BaseSettings):
    DATABASE_URL: str
    DEBUG: bool

    class Config:
        env_file = ".env"

settings = Settings()


def _find_modules(postfix="models"):
    src_dir = pathlib.Path(__file__).resolve().parent.parent / "src"
    modules = []

    for path in src_dir.rglob(f"{postfix}.py"):
        relative_path = path.relative_to(src_dir.parent).with_suffix("")
        module_name = ".".join(relative_path.parts)

        try:
            modules.append(import_module(module_name))
        except ModuleNotFoundError:
            print(f"Не удалось импортировать модуль: {module_name}")
    return modules


def detect_models():
    for module in _find_modules("models"):
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)
            if isinstance(attribute, type) and issubclass(attribute, Base) and attribute is not Base:
                print(f"Detected model: {attribute_name}")
                globals()[attribute_name] = attribute
