from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def configure_logging(log_level: str, log_file_path: str) -> None:
    level = logging.getLevelNamesMapping().get(log_level.upper())
    if level is None:
        raise RuntimeError(f"Invalid LOG_LEVEL: {log_level}")

    os.makedirs(os.path.dirname(log_file_path) or ".", exist_ok=True)

    formatter = JsonFormatter()
    fh = logging.FileHandler(log_file_path, encoding="utf-8")
    fh.setFormatter(formatter)
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)

    logging.basicConfig(level=level, handlers=[fh, sh], force=True)
