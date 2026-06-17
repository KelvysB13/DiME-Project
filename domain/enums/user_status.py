from enum import Enum


class UserStatus(str, Enum):
    PENDING_ACTIVATION = "PENDING_ACTIVATION"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
