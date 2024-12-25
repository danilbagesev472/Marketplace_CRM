import os
from dotenv import load_dotenv
from sqlalchemy import ARRAY, JSON, Boolean, Float, ForeignKey, Table, create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

load_dotenv()

db_env = os.getenv('DATABASE_URL')
# DATABASE_URL = "db://username:passwd@host:port/db_name"
engine = create_engine(db_env)

# Database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


favorites = Table(
    'favorites', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('product_id', Integer, ForeignKey('products.id'))
)


# User model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    password = Column(String)
    roles = Column(JSON, default={"user": True, "admin": False}, nullable=False)
    favorite_products = relationship("Product", secondary=favorites, back_populates="favorited_by")

# Product model
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    img = Column(ARRAY(String), nullable=False)  # Assuming URLs are stored as strings
    gender = Column(ARRAY(String), nullable=False)
    size = Column(ARRAY(String), nullable=False)
    color = Column(ARRAY(String), nullable=False)
    style = Column(ARRAY(String), nullable=False)
    
    favorited_by = relationship("User", secondary=favorites, back_populates="favorite_products")


# Create all tables
Base.metadata.create_all(bind=engine)