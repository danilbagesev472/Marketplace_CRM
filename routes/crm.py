from fastapi import APIRouter, Depends, FastAPI, HTTPException
from model.model import Product
from schems import ProductCreateSchema, ProductSchema
from utils.get_db import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/create_product", response_model=ProductSchema)
def create_product(product: ProductCreateSchema, db: Session = Depends(get_db)):
    db_product = Product(
        name=product.name,
        brand=product.brand,
        description=product.description,
        price=product.price,
        img=product.img,
        gender=product.gender,
        size=product.size,
        color=product.color,
        style=product.style
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.put("/update_product/{product_id}")
def update_product(product_id: int, product: ProductCreateSchema, db: Session = Depends(get_db)):
    # Retrieve the product from the database
    db_product = db.query(Product).filter(Product.id == product_id).first()
    
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Update the product fields
    db_product.name = product.name
    db_product.brand = product.brand
    db_product.description = product.description
    db_product.price = product.price
    db_product.img = product.img
    db_product.gender = product.gender
    db_product.size = product.size
    db_product.color = product.color
    db_product.style = product.style

    db.commit()
    db.refresh(db_product)
    
    return {"product":db_product, "message": "Продукт успешно изменен"  }

@router.delete("/delete_product/{prod_id}")
def delete_product(prod_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == prod_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    db.delete(db_product)
    db.commit()
    return {"message": "Продукт успешно удален"}