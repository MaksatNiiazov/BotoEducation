from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


REQUIRED_VARS = ("APP_HOST", "APP_PORT", "DATABASE_PATH", "BASE_URL", "LOG_LEVEL")


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        name, value = line.split("=", 1)
        name = name.strip()
        value = value.strip()
        if name and name not in os.environ:
            os.environ[name] = value


def main() -> int:
    base_dir = Path(__file__).resolve().parent
    load_env_file(base_dir / "env.example")

    missing = [name for name in REQUIRED_VARS if not os.getenv(name)]
    if missing:
        print(f"Missing required environment variables: {', '.join(missing)}", file=sys.stderr)
        return 1

    command = [
        sys.executable,
        "-m",
        "uvicorn",
        "app.main:app",
        "--host",
        os.environ["APP_HOST"],
        "--port",
        os.environ["APP_PORT"],
    ]
    return subprocess.call(command)


if __name__ == "__main__":
    raise SystemExit(main())
