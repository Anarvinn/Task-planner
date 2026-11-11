# Task Planner

A command-line task management application built with Python. It
supports task creation and editing, priority-based organization, task
status progression, dependency management, searching, and JSON
persistence.

## Overview

Task Planner is a small, modular application for managing tasks and the
relationships between them. It is designed around a clear separation of
responsibilities:

- **Models** define tasks, priorities, statuses, and validation rules.
- **Services** contain task-management logic and dependency checks.
- **Storage** handles loading and saving task data in JSON format.
- **Interfaces** provide the interactive command-line menu.
- **Tests** verify the main model, manager, and enum behaviour.

The application runs locally and stores its data in a JSON file. It does
not require a database server or third-party runtime packages.

## Features

### Task management

- Create tasks with a title and priority.
- Edit an existing task’s title and priority.
- Delete tasks when no other task depends on them.
- Assign each task a unique UUID-based identifier.
- Keep task data between application runs using JSON storage.

### Priorities

Every task has one of three priorities:

| Priority | Meaning          |
| :------- | :--------------- |
| `High`   | Highest priority |
| `Medium` | Normal priority  |
| `Low`    | Lowest priority  |

Tasks are displayed in descending priority order: High, Medium, then
Low.

### Task statuses

A task progresses through the following lifecycle:

```text
New -> In work -> Done
```

The status is advanced one step at a time. A completed task cannot be
advanced further.

### Task dependencies

A task can depend on another task. A task with dependencies is eligible
to start only when all of its dependencies have been completed.

The application checks dependency relationships and prevents several
invalid operations:

- A task cannot depend on itself.
- The same dependency cannot be added more than once.
- Circular dependency chains are rejected.
- A dependency cannot be added to a completed task.
- A task cannot be started while one or more of its dependencies are
  incomplete.
- A task cannot be deleted while another task depends on it.

Dependencies are stored as task identifiers and are restored when the
application starts.

### Searching and task views

- Display all tasks.
- Display tasks whose dependencies are complete and which are not yet
  marked as done.
- Display completed tasks.
- Search tasks by title or identifier.
- Search is case-insensitive.
- Task lists are ordered by priority.

### JSON persistence and data safety

- Task data is stored in `data/tasks.json`.
- If the data file does not exist, the application starts with an empty
  task collection.
- The storage layer checks the JSON structure and detects duplicate task
  identifiers.
- Saving uses a temporary file followed by an atomic replacement of the
  target file.
- Manager operations take a snapshot of the current in-memory task
  collection. If an operation or its save fails, the previous in-memory
  state is restored.

> **Storage format note:** The current implementation uses the JSON key
> `dependence` for the list of dependency IDs. This is the existing
> on-disk schema; changing it requires updating both serialization and
> deserialization code, or adding a migration.

## Project structure

```text
Task-planner/
├── interfaces/
│   ├── console.py
│   └── console_helpers.py
├── models/
│   ├── dependence.py
│   ├── enum.py
│   ├── task.py
│   └── validation_helpers.py
├── services/
│   └── manager.py
├── storage/
│   └── json_storage.py
├── test/
│   ├── conftest.py
│   ├── test_enum.py
│   ├── test_manager.py
│   └── test_task.py
├── data/                 # Created at runtime; ignored by Git
├── exceptions.py
└── main.py
```

### Architecture

| Component                       | Responsibility                                                   |
| :------------------------------ | :--------------------------------------------------------------- |
| `models/task.py`                | Task data model, default values, and task-level operations       |
| `models/enum.py`                | Priority and status enumerations                                 |
| `models/validation_helpers.py`  | Validation and conversion of task input values                   |
| `models/dependence.py`          | Dependency validation and readiness checks                       |
| `services/manager.py`           | Coordinates task operations, sorting, searching, and persistence |
| `storage/json_storage.py`       | Reads and writes task data in JSON format                        |
| `interfaces/console.py`         | Interactive command-line menu                                    |
| `interfaces/console_helpers.py` | Console input and task-list formatting                           |
| `exceptions.py`                 | Application-specific exception hierarchy                         |
| `test/`                         | Automated tests                                                  |

## Requirements

- Python **3.11 or newer**.
- `pytest` to run the test suite.

The application itself uses the Python standard library. No third-party
runtime dependencies are required.

## Installation

Clone the repository:

```bash
git clone https://github.com/Anarvinn/Task-planner.git
cd Task-planner
```

Create and activate a virtual environment (recommended).

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the testing dependency:

```bash
python -m pip install pytest
```

## Run the application

From the project root, run:

```bash
python main.py
```

The application opens an interactive menu. Choose an operation by
entering its number, then follow the prompts to provide the required
task information.

The available menu operations include task creation, editing and
deletion, dependency management, status progression, task views, and
search.

## Run the tests

Run the test suite from the repository root:

```bash
python -m pytest
```

For a more detailed test report:

```bash
python -m pytest -v
```

The current test suite covers:

- Priority ordering and status values.
- Task creation and input validation.
- Valid and invalid task updates.
- Task restoration from JSON storage.
- Sorting and task views.
- Dependency validation and dependency persistence.
- Task status progression.
- Deletion rules and unknown task identifiers.
- Behaviour with empty storage.

Tests use pytest fixtures and the built-in `tmp_path` fixture so
storage-related tests can work with temporary files rather than the
application’s real data file.

## Data format

The storage layer serializes tasks as a JSON array. A record has the
following shape:

```json
[
  {
    "id": "a-uuid-value",
    "title": "Prepare project documentation",
    "priority": "High",
    "status": "New",
    "dependence": []
  }
]
```

The `dependence` field contains identifiers of tasks that must be
completed before the current task can start.

The example is illustrative; actual IDs are generated by the
application.

## Error handling

The application defines custom exceptions derived from `ManagerError`:

- `ValidationError` — invalid task data or an invalid operation.
- `StorageError` — storage or persisted-data problems.
- `DependenceError` — invalid dependency operations.
- `TaskNotFoundError` — requested task identifier does not exist.
- `DuplicateIdError` — duplicate task identifier.

The console interface catches application-level errors and displays an
error message instead of exposing an unhandled traceback for expected
user input or manager errors.

## Design notes

- **Separation of concerns:** the console interface does not own the
  task-management rules; it delegates operations to `Manager`.
- **Typed domain values:** `PriorityType` and `StatusType` are
  represented with `StrEnum`.
- **Dataclass model:** `Task` uses a dataclass and generates a UUID when
  an ID is not supplied.
- **Defensive storage:** JSON data is checked before it is loaded into
  the manager.
- **Safer writes:** a temporary file is used before replacing the
  persisted JSON file.
- **Rollback on failure:** the manager restores its previous in-memory
  task collection if an operation or persistence step raises an
  exception.

## Current scope and limitations

Task Planner is a local command-line application, not a hosted
multi-user service.

- Data is stored in a local JSON file; there is no SQL database.
- There is no graphical interface, web API, authentication, or
  multi-user access.
- The application is intended for one local user/process. It does not
  implement cross-process locking or concurrent-write coordination.
- The dependency list is stored using the current `dependence` JSON
  field name for compatibility with the existing implementation.
