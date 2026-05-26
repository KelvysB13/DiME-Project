from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_maestra_host: str = "localhost"
    db_maestra_port: int = 5432
    db_maestra_name: str = "dime_maestra"
    db_maestra_user: str = "postgres"
    db_maestra_password: str = "changeme"

    db_client_host: str = "localhost"
    db_client_port: int = 5432
    db_client_user: str = "postgres"
    db_client_password: str = "changeme"

    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_secret_key: str = "supersecretkey_change_in_production"
    app_debug: bool = True

    ml_client_id: str = ""
    ml_client_secret: str = ""
    ml_redirect_uri: str = "http://localhost:8000/auth/ml/callback"
    ml_sandbox_mode: bool = True

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

settings = Settings()
