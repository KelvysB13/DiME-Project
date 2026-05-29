from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    
    database_url: str = "postgresql://dime_admin:DiME2K26_$@localhost:5432/dime_maestra"

    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_secret_key: str = "supersecretkey_DiME_2026_change_in_production"
    app_debug: bool = True

    ml_client_id: str = ""
    ml_client_secret: str = ""
    ml_redirect_uri: str = "http://localhost:8000/auth/ml/callback"
    ml_sandbox_mode: bool = True

    metabase_url: str = "http://localhost:3000"
    metabase_user: str = "admin@dime.local"
    metabase_password: str = "admin123"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}

settings = Settings()