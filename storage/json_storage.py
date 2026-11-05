from exceptions import StorageError
from dataclasses import asdict
from models.task import Task
from pathlib import Path
from typing import Any
import tempfile
import json
import os


class JsonStorage:
    def __init__(self, filepath: str | Path) -> None:
        self.filepath = Path(filepath)

    def load(self) -> dict[str, Any]:
        if not self.filepath.exists():
            return {}

        try:
            with self.filepath.open('r', encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise StorageError("Invalid JSON root structure")

            task_map: dict[str, Any] = {}

            for item in data:
                if not isinstance(item, dict):
                    raise StorageError("Invalid task record")

                task = Task(
                    id=item['id'],
                    title=item['title'],
                    priority=item['priority'],
                    status=item['status'],
                    dependence=item['dependence']
                )

                if task.id in task_map:
                    raise StorageError("Duplicate Id in storage")

                task_map[task.id] = asdict(task)

            return task_map
        except StorageError:
            raise

        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
            raise StorageError(f"Cannot load manager data: {e}") from e

    def save(self, tasks: dict[str, Task]) -> None:
        data = [{
            'id': task.id,
            'title': task.title,
            'priority': task.priority,
            'status': task.status,
            'dependence': task.dependence
        }
            for task in tasks.values()]

        tempt_path: Path | None = None

        try:
            self.filepath.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            with tempfile.NamedTemporaryFile(
                mode='w',
                encoding='utf-8',
                dir=self.filepath.parent,
                suffix=".tmp",
                delete=False
            ) as temp_file:
                tempt_path = Path(temp_file.name)

                json.dump(data, temp_file, ensure_ascii=False, indent=4)
                temp_file.flush()
                os.fsync(temp_file.fileno)

            os.replace(tempt_path, self.filepath)
            tempt_path = None
        except OSError as e:
            raise StorageError(
                f"Cannot save manage data: {e}"
            ) from e

        finally:
            if tempt_path is not None:
                tempt_path.unlink(missing_ok=True)
