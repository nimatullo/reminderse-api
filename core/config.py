from pydantic import BaseModel


class Settings(BaseModel):
    PROJECT_NAME: str = "Reminderse API"
    authjwt_secret_key: str = "super-secret-key"
    authjwt_token_location: set = {"cookies", "headers"}
    authjwt_cookie_csrf_protect: bool = False
    authjwt_cookie_secure: bool = True
    authjwt_cookie_samesite: str = "none"
    authjwt_cookie_max_age: int = 60 * 60 * 24  # 1 day
    SECRET_KEY: str = "secret"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day


settings = Settings()
