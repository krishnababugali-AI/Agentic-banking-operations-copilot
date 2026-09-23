from app.core.config import get_settings


def test_settings_load_successfully() -> None:
    settings = get_settings()

    assert settings.app_name == (
        "Agentic Banking Operations Copilot"
    )

    assert settings.ollama_chat_model == "qwen3:4b"

    assert (
        settings.ollama_embedding_model
        == "nomic-embed-text:latest"
    )

    assert settings.api_port == 8000

    assert settings.rag_top_k > 0


def test_runtime_paths_are_absolute() -> None:
    settings = get_settings()

    assert settings.project_root.is_absolute()
    assert settings.chroma_path.is_absolute()
    assert settings.checkpoint_path.is_absolute()