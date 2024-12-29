from datetime import timedelta
from authx import AuthX, AuthXConfig


config = AuthXConfig()
config.JWT_SECRET_KEY = "secret_key"
config.JWT_ACCESS_COOKIE_NAME = "my-cookie"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_ACCESS_TOKEN_EXPIRES= timedelta(minutes=15)
security = AuthX(config=config) 