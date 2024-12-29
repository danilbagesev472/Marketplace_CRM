from sqlalchemy import ARRAY, JSON, Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()

favorites = Table(
    'favorites', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('product_id', Integer, ForeignKey('products.id'))
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    password = Column(String)
    roles = Column(JSON, default={"user": True, "admin": False}, nullable=False)
    favorite_products = relationship("Product", secondary=favorites, back_populates="favorited_by")


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
    
		