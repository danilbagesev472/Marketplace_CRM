from fastapi import APIRouter, Depends, FastAPI, HTTPException
from model.model import Product
from sqlalchemy.orm import Session
from utils.get_db import get_db

router = APIRouter()

@router.get("/products")
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    # Получаем все продукты с пропуском и лимитом
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

@router.get("/products/{product_id}")
def read_product(product_id: int, db: Session = Depends(get_db)):
    # Получаем продукт по id
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    return product