from __future__ import annotations

import logging


def configure_logging(log_level: str) -> None:
    level_name = log_level.upper()
    level_mapping = logging.getLevelNamesMapping()
    if level_name not in level_mapping:
        raise RuntimeError(f"Invalid LOG_LEVEL: {log_level}")

    logging.basicConfig(
        level=level_mapping[level_name],
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        force=True,
    )
