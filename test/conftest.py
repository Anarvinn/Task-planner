from storage.json_storage import JsonStorage
from services.manager import Manager
import pytest


@pytest.fixture
def manager(tmp_path):
    storage = JsonStorage(tmp_path / "test_tasks.json")
    return Manager(storage)


@pytest.fixture
def sample_task(manager):
    return manager.add_task('Test task', 'Low')
