from typing import TypedDict, List, Dict

class ChatState(TypedDict):
    question: str
    answer: str
    route: str
    history: List[Dict]