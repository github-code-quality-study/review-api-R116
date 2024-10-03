from typing import TypedDict
from models.sentiment import Sentiment
class Review(TypedDict):
    ReviewId: str
    ReviewBody: str
    Timestamp: str
    Location: str
    sentiment: Sentiment