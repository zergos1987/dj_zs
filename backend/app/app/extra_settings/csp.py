INSTALLED_APPS = ['csp']
MIDDLEWARE = ['csp.middleware.CSPMiddleware']

CSP_WORKER_SRC = ("'self'", "'unsafe-inline'", 'http: blob:', 'https: blob:',)
CSP_DEFAULT_SRC = ("'none'", "'unsafe-inline'")
CSP_STYLE_SRC = (
    "'self'",
    "'unsafe-inline'",
    'fonts.googleapis.com',
)
CSP_SCRIPT_SRC = (
    "'self'",
    "'unsafe-inline'",
    "https://stackpath.bootstrapcdn.com",
    "https://cdn.jsdelivr.net",
    "https://code.jquery.com",
)
CSP_FONT_SRC = ("'self'", 'fonts.gstatic.com')
CSP_IMG_SRC = ("'self'", "'unsafe-inline'", 'http: data:',  'https: data:')

CSP_INCLUDE_NONCE_IN = [
    "script-src"
]
