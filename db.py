from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

engine = create_engine("sqlite+pysqlite:///database.db")


class Base(DeclarativeBase):
    pass


class Confession(Base):
    __tablename__ = "confessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    confession: Mapped[str] = mapped_column()
    timestamp: Mapped[str] = mapped_column()
    user: Mapped[str] = mapped_column()

    def __repr__(self) -> str:
        return f"Confession(id={self.id!r}, user={self.user!r})"


Base.metadata.create_all(engine)
session = Session(engine)


def uploadConfession(confession, timestamp, user):
    global engine, session
    confession_obj = Confession(
        id=None, confession=confession, timestamp=timestamp, user=user
    )
    session.add(confession_obj)
    session.commit()

    return confession_obj


def getConfession(id):
    global engine, session
    obj = session.scalars(select(Confession).where(Confession.id == int(id))).first()
    print(obj)
    return obj
