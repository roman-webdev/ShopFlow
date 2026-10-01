"""Keep isolated test databases in a writable, unique project-local directory."""
from pathlib import Path
from uuid import uuid4


def pytest_configure(config):
    # Honor an explicit --basetemp supplied by CI or a developer.
    if config.option.basetemp is None:
        root = Path(config.rootpath) / '.pytest-tmp'
        root.mkdir(parents=True, exist_ok=True)
        config.option.basetemp = root / uuid4().hex
