from __future__ import annotations
from storage.json_storage import JsonStorage
from services.manager import Manager
from pathlib import Path
import pytest


@pytest.fixture
def manager(tmp_path: Path):
    storage = JsonStorage(tmp_path / "test_tasks.json")
    return Manager(storage)


@pytest.fixture
def sample_task(manager: Manager):
    return manager.add_task('Test task', 'Low')
