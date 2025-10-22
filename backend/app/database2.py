"""
Database configuration and models for car data
Uses PostgreSQL with SQLAlchemy ORM
"""

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os

# Database URL - use environment variable for security
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/car_database"
)

# Handle postgresql:// vs postgresql+psycopg2://
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Association tables for many-to-many relationships
model_trims = Table(
    'model_trims',
    Base.metadata,
    Column('model_id', Integer, ForeignKey('models.id'), primary_key=True),
    Column('trim_id', Integer, ForeignKey('trims.id'), primary_key=True)
)

model_body_types = Table(
    'model_body_types',
    Base.metadata,
    Column('model_id', Integer, ForeignKey('models.id'), primary_key=True),
    Column('body_type_id', Integer, ForeignKey('body_types.id'), primary_key=True)
)

model_transmissions = Table(
    'model_transmissions',
    Base.metadata,
    Column('model_id', Integer, ForeignKey('models.id'), primary_key=True),
    Column('transmission_id', Integer, ForeignKey('transmissions.id'), primary_key=True)
)

model_fuel_types = Table(
    'model_fuel_types',
    Base.metadata,
    Column('model_id', Integer, ForeignKey('models.id'), primary_key=True),
    Column('fuel_type_id', Integer, ForeignKey('fuel_types.id'), primary_key=True)
)


# Models
class Make(Base):
    __tablename__ = "makes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    models = relationship("Model", back_populates="make", cascade="all, delete-orphan")


class Model(Base):
    __tablename__ = "models"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    make_id = Column(Integer, ForeignKey("makes.id"))
    year_min = Column(Integer)
    year_max = Column(Integer)
    
    make = relationship("Make", back_populates="models")
    trims = relationship("Trim", secondary=model_trims)
    body_types = relationship("BodyType", secondary=model_body_types)
    transmissions = relationship("Transmission", secondary=model_transmissions)
    fuel_types = relationship("FuelType", secondary=model_fuel_types)
    
    __table_args__ = (
        UniqueConstraint('make_id', 'name'),
    )


class Trim(Base):
    __tablename__ = "trims"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)


class BodyType(Base):
    __tablename__ = "body_types"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)


class Transmission(Base):
    __tablename__ = "transmissions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)


class FuelType(Base):
    __tablename__ = "fuel_types"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)
