from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True)
class Settings:
    env: str = os.getenv("CALLSIGNAL_ENV", "local")
    db_path: Path = Path(os.getenv("CALLSIGNAL_DB_PATH", "./signal-server/data/callsignal.db"))
    api_host: str = os.getenv("CALLSIGNAL_API_HOST", "127.0.0.1")
    api_port: int = int(os.getenv("CALLSIGNAL_API_PORT", "8088"))
    public_api_base_url: str = os.getenv("PUBLIC_API_BASE_URL", "http://127.0.0.1:8088")


def get_settings() -> Settings:
    return Settings()
