
class ManagerError(Exception):
    """Base exception for manager operations"""


class ValidationError(ManagerError):
    """Invalid input or entity data"""


class StorageError(ManagerError):
    """"Storage operation failed"""


class DependenceError(ManagerError):
    """Dependency connection error"""


class TaskNotFoundError(ManagerError):
    """Task not found"""


class DuplicateIdError(ManagerError):
    """ID already exist"""
