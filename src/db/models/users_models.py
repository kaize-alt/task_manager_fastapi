from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base
from .tasks_models import TasksOrm


class UsersOrm(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    age: Mapped[int] = mapped_column(Integer)
    bio: Mapped[str] = mapped_column(String(255), nullable=True)

    tasks = relationship("TasksOrm", back_populates="user")
