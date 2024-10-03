import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from urllib.parse import parse_qs, urlparse
import json
import pandas as pd
from datetime import datetime
import uuid
import os
from typing import Callable, Any
from wsgiref.simple_server import make_server
from server_utils.route import ROUTES
from server_utils.request import Request
from server_utils.response import Response
import controller

nltk.download('vader_lexicon', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('stopwords', quiet=True)

adj_noun_pairs_count = {}
sia = SentimentIntensityAnalyzer()
stop_words = set(stopwords.words('english'))

reviews = pd.read_csv('data/reviews.csv').to_dict('records')
#decorator
class ReviewAnalyzerServer:
    def __init__(self) -> None:
        # This method is a placeholder for future initialization logic
        pass
    
    def analyze_sentiment(self,review_body):
        sentiment_scores = sia.polarity_scores(review_body)
        return sentiment_scores

    def __call__(self, environ: dict[str, Any], start_response: Callable[..., Any]) -> bytes:
        """
        The environ parameter is a dictionary containing some useful
        HTTP request information such as: REQUEST_METHOD, CONTENT_LENGTH, QUERY_STRING,
        PATH_INFO, CONTENT_TYPE, etc.
        """
        method = environ["REQUEST_METHOD"]
        path = environ["PATH_INFO"]
        if path not in ROUTES:
            start_response("404 Not Found", [])
            return [b"404 Not Found"]
        if method not in ROUTES[path]:
            start_response("405 Method Not Allowed", [])
            return [b"405 Method Not Allowed"]
        handler = ROUTES[path][method]
        request = Request(environ, self.analyze_sentiment)
        response:Response = handler(request)
        start_response(response.status, response.headers)
        return [json.dumps(response.body).encode("utf-8")]

if __name__ == "__main__":
    app = ReviewAnalyzerServer()
    port = os.environ.get('PORT', 8000)
    with make_server("", port, app) as httpd:
        print(f"Listening on port {port}...")
        httpd.serve_forever()