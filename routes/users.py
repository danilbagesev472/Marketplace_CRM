from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from model.model import User
from schems import UserSchema
from utils.get_db import get_db
from utils.auth import security, config


router = APIRouter()


@router.post("/register")
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

@router.post("/login")
def login(cred: UserSchema,response: Response, db: Session = Depends(get_db) ):
    user = db.query(User).filter(User.email == cred.email, User.password == cred.password).first()

    if user is not None:

        long_term_token = security.create_access_token(uid=f"{user.id}", expires_delta=timedelta(days=30))

        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, long_term_token, httponly=True)
        
        return {"data":user,"access_token": long_term_token}
    raise HTTPException(status_code=401, detail="Неверный логин или пароль")


@router.get("/logout",dependencies=[Depends(security.access_token_required)])
def logout(response: Response):
    response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME)

    return {"message": "Выход из системы успешен"}

@router.get("/users", dependencies=[Depends(security.access_token_required)])
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
