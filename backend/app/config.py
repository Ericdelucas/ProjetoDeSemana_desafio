from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """
    Centraliza todas as configurações do sistema.
    Os valores são carregados automaticamente do arquivo .env
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ===== APLICAÇÃO =====
    app_name: str = Field(default="SmartSaude SUS", alias="APP_NAME")
    env: str = Field(default="dev", alias="ENV")
    cors_origins: str = Field(default="http://localhost:5173", alias="CORS_ORIGINS")

    # ===== BANCO DE DADOS =====
    db_host: str = Field(default="127.0.0.1", alias="DB_HOST")
    db_port: int = Field(default=3306, alias="DB_PORT")
    db_user: str = Field(default="root", alias="DB_USER")
    db_password: str = Field(default="", alias="DB_PASSWORD")
    db_name: str = Field(default="smartsaude", alias="DB_NAME")

    # ===== IA GENERATIVA =====
    # Providers possíveis: "google" (gemini), "groq" (llama), "mock" (fallback local)
    ai_provider: str = Field(default="mock", alias="AI_PROVIDER")
    ai_key: str | None = Field(default=None, alias="AI_KEY")
    ai_model: str = Field(default="llama-3.1-8b-instant", alias="AI_MODEL")

    def database_url(self) -> str:
        """
        Monta a URL de conexão com o MySQL
        """
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
            f"?charset=utf8mb4"
        )


# Instância única de configurações (singleton)
settings = Settings()
