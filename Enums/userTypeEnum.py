from enum import Enum

class UserType(str, Enum):
    Vet = "Vet"
    Owner = "Owner"