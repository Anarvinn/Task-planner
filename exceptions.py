
class ManagerError(Exception):
    """Base exception for manager operations"""


class ValidationError(ManagerError):
    """Invalid input or entity data"""


class StorageError(ManagerError):
    """"Storage operation failed"""
