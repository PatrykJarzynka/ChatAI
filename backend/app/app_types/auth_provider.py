from enum import Enum

class AuthProvider(str, Enum):
    GOOGLE = "google"
    LOCAL = "local"