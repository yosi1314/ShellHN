import logging


def parse_api_call(func):
    def inner(*args, **kwargs):
        res = func(*args, **kwargs)
        log_msg = f"The url: {res.url} returned the status code: {res.status_code}"
        if res.status_code != 200:
            log_msg = log_msg + f" with the following message: {res.json()}"
            logging.exception(log_msg)
            return
        logging.info(log_msg)
        return res.json()

    return inner
