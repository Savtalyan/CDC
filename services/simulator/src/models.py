from datetime import datetime 
from sqlalchemy import ForeignKey, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass 


class User(Base):
    __tabelname__ = "users"

    id :            Mapped[int] = mapped_column(primary_key=True)
    u_first_name :  Mapped[str] = mapped_column(String(64))
    u_last_name :   Mapped[str] = mapped_column(String(64))
    u_email :       Mapped[str] = mapped_column(String(64), unique=True)
    u_phone :       Mapped[str] = mapped_column(String(24), unique=True)
    u_city :        Mapped[str] = mapped_column(String(24))
    u_country :     Mapped[str] = mapped_column(String(24))
    u_postal :      Mapped[str] = mapped_column(String(14))
    
    posts :         Mapped[list["Post"]] = relationship(back_populates="user", passive_delete=True)


    @property
    def full_name(self):
        return f"{self.u_first_name} {self.u_last_name}"
    


class Post(Base):
    __tablename__ = "posts"

    id :            Mapped[int] = mapped_column(primary_key=True)
    user_id :       Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="cascade"))
    title :         Mapped[str] = mapped_column(String(64))
    content :       Mapped[str] = mapped_column(String(255))
    created_at :    Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at :    Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    user :          Mapped["User"] = relationship(back_populates="post")

