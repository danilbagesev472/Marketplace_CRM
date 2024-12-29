from typing import Dict, List
from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from typing import List

class GenderEnum(str, Enum):
    man = "man"
    woman = "woman"

class SizeEnum(str, Enum):
    xs = "xs"
    s = "s"
    m = "m"
    l = "l"
    xl = "xl"
    xxl = "2xl"
    xxxl = "3xl"
    xxxxl = "4xl"

class ColorEnum(str, Enum):
    black = "black"
    white = "white"
    red = "red"
    blue = "blue"
    green = "green"

class StyleEnum(str, Enum):
    casual = "casual"
    formal = "formal"
    sportswear = "sportswear"
    children = "children"
    accessories = "accessories"

class ImgEnum(str, Enum):
    img = ["https://recrentshop.ru/d/003-01_hudi.jpg", "https://recrentshop.ru/d/801.png"]

class ProductCreateSchema(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    brand: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=3, max_length=1000)
    price: float = Field(gt=0)
    img: List[str] = Field(default_factory=lambda: [ImgEnum.img])
    gender: List[GenderEnum] = Field(default_factory=lambda: [GenderEnum.man, GenderEnum.woman])
    size: List[SizeEnum] = Field(default_factory=lambda: [SizeEnum.xs, SizeEnum.s, SizeEnum.m, SizeEnum.l, SizeEnum.xl, SizeEnum.xxl, SizeEnum.xxxl, SizeEnum.xxxxl])
    color: List[ColorEnum] = Field(default_factory=lambda: [ColorEnum.black, ColorEnum.white, ColorEnum.red, ColorEnum.blue, ColorEnum.green])
    style: List[StyleEnum] = Field(default_factory=lambda: [StyleEnum.casual, StyleEnum.formal, StyleEnum.sportswear, StyleEnum.children, StyleEnum.accessories])

    class Config:
        use_enum_values = True  

class ProductSchema(ProductCreateSchema):
    id: int

class UserSchema(BaseModel):
    id: int
    name: str = Field(default="default_user", alias="user_name")
    phone: str = Field(default="88005553535", alias="user_phone", len=11)
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)
    roles: Dict[str, bool] = Field(default={"user": True, "admin": False}, alias="user_roles")
    # favorite_products: List[ProductSchema] = []

