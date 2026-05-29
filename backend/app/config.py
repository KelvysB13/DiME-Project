from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_secret_key: str = "supersecretkey_change_in_production"
    app_debug: bool = True

    ml_client_id: str = ""
    ml_client_secret: str = ""
    ml_redirect_uri: str = "http://localhost:8000/auth/ml/callback"
    ml_sandbox_mode: bool = True

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}

settings = Settings()
