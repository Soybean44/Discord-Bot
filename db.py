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


Base.metadata.create_all(engine)


def uploadConfession(confession, timestamp, user):
    global engine
    confession_obj = Confession(
        id=None, confession=confession, timestamp=timestamp, user=user
    )
    with Session(engine) as session:
        session.add(confession_obj)
        session.commit()

    return confession_obj

def getConfession(ID):
    global engine
    stmt = select(Confession).with(Confession.id == ID)
    confessions = []
    with Session(engine) as session:
        for row in session.exec(stmt):
            confessions.append(row)
    if len(confessions) > 0:
        return confessions[0]
    else:
        return None