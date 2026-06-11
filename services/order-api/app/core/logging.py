import logging
import logging.config
import os
from typing import Any, Dict

from pythonjsonlogger import jsonlogger

class JsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter to inject clean level names and logger origins."""
    def add_fields(self, log_record: Dict[str, Any], record: logging.LogRecord, message_dict: Dict[str, Any]) -> None:
        super().add_fields(log_record, record, message_dict)
        log_record.setdefault("level", record.levelname)
        log_record.setdefault("logger", record.name)


def configure_logging() -> None:
    """Configures system-wide logging including Uvicorn overrides."""
    # Toggle between "json" and "standard" via environment variables
    formatter = os.getenv("LOG_FORMATTER", "standard")
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "json": {
                "()": JsonFormatter,
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": formatter,
                "stream": "ext://sys.stdout",
            }
        },
        "loggers": {
            # Route internal FastAPI/Uvicorn loggers through your handler
            "uvicorn": {
                "handlers": ["console"],
                "level": log_level,
                "propagate": False
            },
            "uvicorn.error": {
                "handlers": ["console"],
                "level": log_level,
                "propagate": False
            },
            "uvicorn.access": {
                "handlers": ["console"],
                "level": log_level,
                "propagate": False
            },
        },
        "root": {
            "handlers": ["console"],
            "level": log_level
        },
    }

    logging.config.dictConfig(config)
