from typing import TypedDict

class Sentiment(TypedDict):
    neg: float
    neu: float
    pos: float
    compound: float