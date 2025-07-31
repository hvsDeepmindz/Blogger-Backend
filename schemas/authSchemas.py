from pydantic import BaseModel
from pydantic_settings import BaseSettings


class AuthSettings(BaseSettings):
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1500
    valid_username: str
    valid_password: str

    class Config:
        env_file = ".env"
        case_sensitive = False


class TokenResponse(BaseModel):
    message: str
    access_token: str
    token_type: str
