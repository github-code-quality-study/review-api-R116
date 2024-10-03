class Response:
    def __init__(self, status_code:int, body:dict):
        if status_code==200:
            self.status = "200 OK"
        if status_code==201:
            self.status = "201 Created"
        if status_code==405:
            self.status = "405 Method Not Allowed"
        if status_code==404:
            self.status = "404 Not Found"
        if status_code==500:
            self.status = "500 Internal Server Error"
        if status_code==400:
            self.status = "400 Bad Request"
        self.body = body
        self.headers = [("Content-Type", "application/json")]