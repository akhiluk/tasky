from tasky.database import Base
from sqlalchemy import String, Integer, Boolean, TIMESTAMP, ForeignKey, DATE
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import text
from typing import List
from pydantic import EmailStr
import datetime

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, name = "id")
    username: Mapped[str] = mapped_column(String(20), nullable = False, unique = True, name = "username")
    email: Mapped[EmailStr] = mapped_column(String(50), nullable = False, unique = True, name = "email")
    password: Mapped[str] = mapped_column(String(100), nullable = False, name = "password")
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone = True), nullable = False, server_default = text("NOW()"), name = "created_at")

    lists: Mapped[List["TaskList"]] = relationship(back_populates = "user", cascade = "all")
    tasks: Mapped[List["Task"]] = relationship(back_populates = "user", cascade = "all")

    def __repr__(self):
        return self.username
    
class TaskList(Base):
    __tablename__ = "lists"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, name = "id")
    name: Mapped[str] = mapped_column(String(25), nullable = False, name = "name")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete = "CASCADE"))

    user: Mapped["User"] = relationship(back_populates = "lists")
    tasks: Mapped[List["Task"]] = relationship(back_populates = "list", cascade = "all")

    def __repr__(self):
        return f"{self.name} - {self.user.username}"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, name = "id")
    title: Mapped[str] = mapped_column(String(50), nullable = False, name = "title")
    details: Mapped[str] = mapped_column(String(250), nullable = True, name = "details")
    is_completed: Mapped[bool] = mapped_column(Boolean, nullable = False, server_default = text("FALSE"), name = "is_completed")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete = "CASCADE"))
    list_id: Mapped[int] = mapped_column(ForeignKey("lists.id", ondelete = "CASCADE"))
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone = True), nullable = False, server_default = text("NOW()"), name = "created_at")

    user: Mapped["User"] = relationship(back_populates = "tasks")
    list: Mapped["TaskList"] = relationship(back_populates = "tasks")

    def __repr__(self):
        return f"{self.id}: {self.name}"