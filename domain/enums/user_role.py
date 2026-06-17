from enum import Enum


class UserRole(str, Enum):
    SUPER_ADMIN = "SuperAdmin"
    ADMIN = "Admin"
    USER = "User"
