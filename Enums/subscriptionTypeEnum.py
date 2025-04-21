from enum import Enum

class SubscriptionType(str, Enum):
    Basic = "Basic"
    Advanced = "Advanced"
    Pro = "Pro"