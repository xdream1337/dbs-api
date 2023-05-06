from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Table, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4
from sqlalchemy.dialects.postgresql import ENUM


Base = declarative_base()


class InstanceTypeEnum(str, Enum):
    physical = "physical"
    ebook = "ebook"
    audiobook = "audiobook"


instance_type_enum = ENUM("physical", "ebook", "audiobook", name="instance_type_enum")
rental_status_enum = ENUM("active", "returned", "overdue", name="rental_status_enum")
instance_status_enum = ENUM("available", "reserved", name="instance_status_enum")
card_status_enum = ENUM("active", "inactive", name="card_status_enum")


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False
    )
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    birth_date = Column(Date, nullable=False)
    personal_identificator = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    publication_id = Column(
        UUID(as_uuid=True), ForeignKey("publications.id"), nullable=False
    )
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)


class Rental(Base):
    __tablename__ = "rentals"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    publication_instance_id = Column(
        UUID(as_uuid=True), ForeignKey("publication_instances.id"), nullable=False
    )
    duration = Column(Integer, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(rental_status_enum, nullable=False)

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)


class Card(Base):
    __tablename__ = "cards"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False
    )
    user_id = Column(UUID(as_uuid=True), nullable=False)
    magstripe = Column(String(20), nullable=False)
    status = Column(card_status_enum, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)


# Association tables
publication_authors = Table(
    "publication_authors",
    Base.metadata,
    Column(
        "publication_id",
        UUID(as_uuid=True),
        ForeignKey("publications.id"),
        primary_key=True,
    ),
    Column("author_id", UUID(as_uuid=True), ForeignKey("authors.id"), primary_key=True),
)

publication_categories = Table(
    "publication_categories",
    Base.metadata,
    Column(
        "publication_id",
        UUID(as_uuid=True),
        ForeignKey("publications.id"),
        primary_key=True,
    ),
    Column(
        "category_id", UUID(as_uuid=True), ForeignKey("categories.id"), primary_key=True
    ),
)


class Author(Base):
    __tablename__ = "authors"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False
    )
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)


class Category(Base):
    __tablename__ = "categories"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False
    )
    name = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)


class Publication(Base):
    __tablename__ = "publications"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False
    )
    title = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)


class Instance(Base):
    __tablename__ = "publication_instances"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False
    )
    type = Column(instance_type_enum, nullable=False)
    publisher = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    status = Column(instance_status_enum, nullable=False)

    publication_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)
