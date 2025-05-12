from enum import Enum

class Tenant(str, Enum):
    MICROSOFT = 'microsoft'
    GOOGLE = "google"
    LOCAL = "local"