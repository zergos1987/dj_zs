INSTALLED_APPS = ['drf_yasg']
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': True,
    'SHOW_REQUEST_HEADERS': True,
    'JSON_EDITOR': True,
    'SUPPORTED_SUBMIT_METHODS': [],
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        },
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
   }
}
