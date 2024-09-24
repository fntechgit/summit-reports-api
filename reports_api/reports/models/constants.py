from enum import Enum

class PresentationStatus(str, Enum):
    RECEIVED = "Received"

class SelectionStatus(str, Enum):
    SELECTED = "selected"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    ALTERNATE = "alternate"
    LIGHTNING_ACCEPTED = "lightning-accepted"
    LIGHTNING_ALTERNATE = "lightning-alternate"

class SubmissionStatus(str, Enum):
    ACCEPTED = "accepted"
    RECEIVED = "received"
    NON_RECEIVED = "nonreceived"

class PresentationListType(str, Enum):
    GROUP = "Group"
    INDIVIDUAL = "Individual"

class PresentationListClass(str, Enum):
    SESSION = "Session"
    LIGHTNING = "Lightning"

class SelectedPresentationCollection(str, Enum):
    SELECTED = "selected"