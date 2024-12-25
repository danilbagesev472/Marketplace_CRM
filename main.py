from schems import ProductCreateSchema, ProductSchema, UserSchema
from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, Response
from authx import AuthX, AuthXConfig 
from db import SessionLocal, User, Product
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="API маркеплейса",
    description="API open source",
    version="1.0.0",
    
)
origins = ["*",]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows requests from these origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

config = AuthXConfig()
config.JWT_SECRET_KEY = "secret_key"
config.JWT_ACCESS_COOKIE_NAME = "my-cookie"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_ACCESS_TOKEN_EXPIRES= timedelta(minutes=15)

security = AuthX(config=config) 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register", tags=["UsersActions"])
def register(cred: UserSchema, db: Session = Depends(get_db)):
    try:
        exist_usr = db.query(User).filter(User.email == cred.email).first()

        if exist_usr is not None:
            raise HTTPException(status_code=400, detail="Пользователь с таким email уже зарегистрирован")
        
        new_user = User(name=cred.name, email=cred.email, phone=cred.phone, password=cred.password, roles="user")

        # uuid = random.randint(1, 999999)
        # token = security.create_access_token(uid=f"{uuid}")
        # response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)

        db.add(new_user)
        db.commit()
    finally:
        db.close()
    return {"message": "Пользователь успешно зарегистрирован"}

@app.post("/login", tags=["UsersActions"])
def login(cred: UserSchema,response: Response, db: Session = Depends(get_db) ):
    user = db.query(User).filter(User.email == cred.email, User.password == cred.password).first()

    if user is not None:

        long_term_token = security.create_access_token(uid=f"{user.id}", expires_delta=timedelta(days=30))

        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, long_term_token, httponly=True)
        
        return {"data":user,"access_token": long_term_token}
    raise HTTPException(status_code=401, detail="Неверный логин или пароль")

@app.get("/logout",dependencies=[Depends(security.access_token_required)], tags=["UsersActions"])
def logout(response: Response):
    response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME)

    return {"message": "Выход из системы успешен"}

@app.get("/users",tags=["UsersActions"], dependencies=[Depends(security.access_token_required)])
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@app.get("/products", tags=["ProductsActions"])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    # Получаем все продукты с пропуском и лимитом
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

@app.get("/products/{product_id}", tags=["ProductsActions"])
def read_product(product_id: int, db: Session = Depends(get_db)):
    # Получаем продукт по id
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    return product


@app.post("/create_product", response_model=ProductSchema, tags=["CrmActions"])
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

@app.put("/update_product/{product_id}",  tags=["CrmActions"])
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

@app.delete("/delete_product/{prod_id}", tags=["CrmActions"])
def delete_product(prod_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == prod_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    db.delete(db_product)
    db.commit()
    return {"message": "Продукт успешно удален"}