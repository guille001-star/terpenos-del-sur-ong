import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

class Settings(BaseModel):
    PROJECT_NAME: str = "Terpenos del Sur API"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    FRONTEND_URL: str = "http://localhost:3000"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = Settings(
    POSTGRES_USER=os.getenv("POSTGRES_USER"),
    POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD"),
    POSTGRES_DB=os.getenv("POSTGRES_DB"),
    POSTGRES_HOST=os.getenv("POSTGRES_HOST", "localhost"), # <-- ESTA LÍNEA FALTABA
    POSTGRES_PORT=os.getenv("POSTGRES_PORT", "5432"),      # <-- ESTA LÍNEA FALTABA
    FRONTEND_URL=os.getenv("FRONTEND_URL", "http://localhost:3000")
)
