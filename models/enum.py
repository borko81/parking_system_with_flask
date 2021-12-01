"""
Use return self.value, because it Enum class, think it is more good, then import third party import
"""

from enum import Enum


class TarifTypeEnum(Enum):
    """
    Enum usage in tariftype model
    """

    common = "Common"
    vip = "Vip"

    def __str__(self):
        return self.value


class UserType(Enum):
    """
    Enum usage in User model to declare what type is it.
    """

    staff = "Staff"
    admin = "Admin"

    def __str__(self):
        return str(self.value)
