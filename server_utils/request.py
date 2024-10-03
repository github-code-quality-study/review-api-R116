from urllib.parse import parse_qs
from typing import Callable
import json
class Request:
    def __init__(self,environ, analyze_sentiment:Callable) -> None:
        self.method = environ["REQUEST_METHOD"]
        self.path = environ["PATH_INFO"]
        self.query = parse_qs(environ["QUERY_STRING"])
        content_length = environ.get("CONTENT_LENGTH", "0")
        if content_length:
            content_length = int(content_length)
        else:
            content_length = 0
        body = environ["wsgi.input"].read(content_length).decode("utf-8")
        if environ.get("CONTENT_TYPE") == "application/json" and body:
            try:
                self.body = json.loads(body)
            except json.JSONDecodeError:
                self.body = {}
        elif environ.get("CONTENT_TYPE") == "application/x-www-form-urlencoded" and body:
            self.body = parse_qs(body)
        else:
            self.body = {}
        self.headers = {key[5:].replace("_", "-").title(): value for key, value in environ.items() if key.startswith("HTTP_")}
        self.analyze_sentiment = analyze_sentiment