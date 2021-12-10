
def parse_api_call(func):
    def inner(*args, **kwargs):
        res = func(*args, **kwargs)