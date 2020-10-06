import uvicorn
from src.server.core.config import ConfigManager


cfg = ConfigManager()


if __name__ == "__main__":

    uvicorn.run(
        "server.app:app",
        host="0.0.0.0",
        port=cfg.api["PORT"],
        log_config=cfg.uvicorn["LOG_CONFIG"],
        reload=cfg.uvicorn["RELOAD"],
        log_level=cfg.uvicorn["LOG_LEVEL"],
    )
