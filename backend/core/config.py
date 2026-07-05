from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    
    supabase_url: str
    supabase_key: str
    supabase_project_url: str

    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_secret_key: str
    app_debug: bool = True

    model_config = {
        
        "env_file": str(Path(__file__).resolve().parent.parent.parent / ".env"),
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }

settings = Settings()
