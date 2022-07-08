from enum import unique
import databases
import ormar
import sqlalchemy
from typing import Optional, List

from .config import settings

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()

class BaseMeta(ormar.ModelMeta):
    database = database
    metadata = metadata

class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = "users"

    id: int = ormar.Integer(primary_key=True)
    email: str = ormar.String(max_length=128, unique=True, nullable=False)
    fname: str = ormar.String(max_length=128, nullable=True)
    lname: str = ormar.String(max_length=128, nullable=True)
    active: bool = ormar.Boolean(default=True, nullable=False)

class UserCreate(User):
    password: str = ormar.String(max_length=128, nullable=False)

class Report(ormar.Model):
    class Meta(BaseMeta):
        tablename = "reports"

    id: int = ormar.Integer(primary_key=True)
    user: User = ormar.ForeignKey(User, nullable=False, orders_by=["lname"], related_orders_by=["id"])
    service_hours: int = ormar.Integer(nullable=False)
    service_mintues: int = ormar.Integer(nullable=False)
    placements: int = ormar.Integer(nullable=False)
    videos: int = ormar.Integer(nullable=False)
    return_visits: int = ormar.Integer(nullable=False)
    bible_studies: int = ormar.Integer(nullable=False)
    notes: str = ormar.String(max_length=256, nullable=False)

engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)