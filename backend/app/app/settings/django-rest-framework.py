"""
Throttling is similar to permissions, in that it determines if a request should be authorized.
Throttles indicate a temporary state, and are used to control the rate of requests that clients can make to an API.
"""
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '15/minute',
        'user': '100/minute'
    }
}