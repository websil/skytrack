import os
import importlib.util
from pathlib import Path
from typing import Callable

from sqlalchemy import create_engine as _sa_create_engine
from sqlalchemy.schema import MetaData
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, Session as SQLAlchemySession
from envparse import env

env.read_envfile('.env')

__all__ = [
    "transactional_session",
    "DatabaseManager",
    "db",
]


class DatabaseNotInitialized(Exception):
    def __init__(self, *args, **kwargs):
        super(DatabaseNotInitialized, self).__init__(args, kwargs)


class transactional_session:
    def __init__(self, expire_on_commit: bool = True):
        if db.Session is None or db.OnCommitExpiringSession is None:
            raise DatabaseNotInitialized("The global database.db singleton is not initialized!")

        self._session = None
        self._expire_on_commit = expire_on_commit

    def __enter__(self) -> SQLAlchemySession:
        if self._expire_on_commit is True:
            self._session = db.OnCommitExpiringSession()
        else:
            self._session = db.Session()

        return self._session

    def __exit__(self, exc_type, exc, tb):
        try:
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise e
        finally:
            self._session.close()


class DatabaseManager:
    def __init__(self):
        self._engine = None
        self._metadata = MetaData()

        self.Session = None
        self.OnCommitExpiringSession = None
        self.BaseModel = declarative_base()

    @property
    def engine(self) -> Engine:
        return self._engine

    @classmethod
    def create_database_engine(cls) -> Engine:
        db_string = "postgres://{}:{}@{}:{}/{}" \
            .format(
                env.str('POSTGRES_USER'),
                env.str('POSTGRES_PASSWORD'),
                env.str('POSTGRES_HOST'),
                env.int('POSTGRES_PORT'),
                env.str('POSTGRES_DB')
            )

        return _sa_create_engine(db_string, encoding='utf-8')

    def initialize(self, db_engine: Engine = None, scope_function: Callable = None):
        if db_engine is None:
            self._engine = self.create_database_engine()
        else:
            self._engine = db_engine

        self.Session = scoped_session(
            sessionmaker(bind=self._engine, expire_on_commit=False),
            scopefunc=scope_function)

        self.OnCommitExpiringSession = scoped_session(
            sessionmaker(bind=self._engine, expire_on_commit=True),
            scopefunc=scope_function)

        import_all_models()

    def cleanup(self):

        if self._engine is not None:
            self._engine.dispose()


def _package_contents(package_name):
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        return set()
    pathname = Path(spec.origin).parent
    ret = set()
    with os.scandir(pathname) as entries:
        for entry in entries:
            if entry.name.startswith('__'):
                continue
            current = '.'.join((package_name, entry.name.partition('.')[0]))
            if entry.is_file():
                if entry.name.endswith('.py'):
                    ret.add(current)
            elif entry.is_dir():
                ret.add(current)
                ret |= _package_contents(current)

    return ret


def import_all_models():
    for full_module_name in _package_contents('app.common.models'):
        importlib.import_module(full_module_name)


db = DatabaseManager()
