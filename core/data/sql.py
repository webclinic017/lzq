# -*- coding: UTF-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from threading import Lock

from core.common.config import Config

engine = create_engine(
    Config.DB_URL,
    echo=False,
    encoding="utf-8",
)
Session = scoped_session(sessionmaker(bind=engine))
ModelBase = declarative_base()
lock = Lock()

@contextmanager
def safe_sessionmaker(session=Session()):
    try:
        lock.acquire()
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        lock.release()
        session.close()
