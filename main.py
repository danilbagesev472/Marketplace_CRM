from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import crm, products, users

app = FastAPI(
    title="API маркеплейса",
    description="API open source",
    version="1.0.0",
    
)
origins = ["*",]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(crm.router, prefix="/crm", tags=["CRM"])

