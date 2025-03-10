from enum import Enum

class Tenant(str, Enum):
    GOOGLE = "google"
    LOCAL = "local"