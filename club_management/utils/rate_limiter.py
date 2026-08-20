import time
from collections import defaultdict
from exceptions.custom import TooManyRequestsException

LOGIN_MAX_ATTEMPTS = 5
LOGIN_WINDOW_SECONDS = 60

_login_attempts = defaultdict(list)

def check_login_rate_limit(key: str):
    now = time.time()
    attempts = _login_attempts[key]
    attempts[:] = [timestamp for timestamp in attempts if now - timestamp < LOGIN_WINDOW_SECONDS]

    if len(attempts) >= LOGIN_MAX_ATTEMPTS:
        raise TooManyRequestsException(
            "Too many login attempts, please try again later"
        )

    attempts.append(now)
