from enum import Enum


class ComplaintCategory(str, Enum):
    TECHNICAL = "техническая"
    PAYMENT = "оплата"
    OTHER = "другое"
