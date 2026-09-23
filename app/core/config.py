from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """
    Central application configuration.

    Configuration values are loaded from environment variables
    and the local .env file during development.

    Other application modules should depend on this settings
    object instead of reading environment variables directly.
    """

    # --------------------------------------------------------
    # Application
    # --------------------------------------------------------

    app_name: str = "Agentic Banking Operations Copilot"

    app_env: Literal[
        "development",
        "testing",
        "production",
    ] = "development"

    app_version: str = "0.1.0"

    debug: bool = True

    api_host: str = "0.0.0.0"

    api_port: int = Field(
        default=8000,
        ge=1,
        le=65535,
    )

    # --------------------------------------------------------
    # Ollama
    # --------------------------------------------------------

    ollama_base_url: str = "http://localhost:11434"

    ollama_chat_model: str = "qwen3:4b"

    ollama_embedding_model: str = "nomic-embed-text:latest"

    llm_temperature: float = Field(
        default=0.0,
        ge=0.0,
        le=2.0,
    )

    # --------------------------------------------------------
    # Application Database
    # --------------------------------------------------------

    database_url: str = "sqlite:///runtime/banking.db"

    # --------------------------------------------------------
    # LangGraph
    # --------------------------------------------------------

    checkpoint_database_path: str = "runtime/checkpoints.db"

    # --------------------------------------------------------
    # Vector Store / RAG
    # --------------------------------------------------------

    chroma_persist_directory: str = "runtime/chroma"

    chroma_collection_name: str = "banking_policies"

    rag_top_k: int = Field(
        default=4,
        ge=1,
        le=20,
    )

    # --------------------------------------------------------
    # LangSmith
    # --------------------------------------------------------

    langsmith_tracing: bool = False

    langsmith_api_key: str | None = None

    langsmith_project: str = (
        "agentic-banking-operations-copilot"
    )

    # --------------------------------------------------------
    # Logging
    # --------------------------------------------------------

    log_level: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"

    # --------------------------------------------------------
    # Pydantic Settings Configuration
    # --------------------------------------------------------

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def project_root(self) -> Path:
        """
        Absolute path to the project root.
        """
        return PROJECT_ROOT

    @property
    def chroma_path(self) -> Path:
        """
        Absolute path to the persistent Chroma directory.
        """
        return PROJECT_ROOT / self.chroma_persist_directory

    @property
    def checkpoint_path(self) -> Path:
        """
        Absolute path to the LangGraph checkpoint database.
        """
        return PROJECT_ROOT / self.checkpoint_database_path


@lru_cache
def get_settings() -> Settings:
    """
    Return one cached Settings instance for the application.
    """
    return Settings()