from typing import Callable
from collections import defaultdict
ROUTES = defaultdict(dict)
def route(path:str,method:str="GET"):
    def decorator(func:Callable):
        ROUTES[path][method] = func
        return func
    return decorator