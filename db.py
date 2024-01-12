from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

engine = create_engine("sqlite+pysqlite:///database.db")


class Base(DeclarativeBase):
    pass


class Confession(Base):
    __tablename__ = "confessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    confession: Mapped[str] = mapped_column()
    timestamp: Mapped[str] = mapped_column()


Base.metadata.create_all(engine)
