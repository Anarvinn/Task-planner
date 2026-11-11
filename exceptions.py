
class ManagerError(Exception):
    """Base exception for manager operations"""


class ValidationError(ManagerError):
    """Invalid input or entity data"""


class StorageError(ManagerError):
    """Storage operation failed"""


class DependencyError(ManagerError):
    """Dependency connection error"""


class TaskNotFoundError(ManagerError):
    """Task not found"""


class DuplicateTaskIdError(ManagerError):
    """ID already exists"""
