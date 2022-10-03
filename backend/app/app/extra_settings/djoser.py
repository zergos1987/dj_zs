INSTALLED_APPS = ['djoser']
DJOSER = {
    'LOGIN_FIELD': 'username',
    'TOKEN_MODEL': None,  # needed for JWT
    'PERMISSIONS': {
        'user_delete': ['app_accounts.permissions.IsAdminUser'],
    },
    # 'HIDE_USERS': If set to True, listing /users/ enpoint by normal user will return only that user’s
    # profile in the list. Beside that, accessing /users/<id>/ endpoints by user without
    # proper permission will result in HTTP 404 instead of HTTP 403.
    'HIDE_USERS': True,
    'ACTIVATION_URL': 'accounts/activation/{uid}/{token}',  # TODO: urls in frontend, POST to back
    'PASSWORD_RESET_CONFIRM_URL': 'accounts/password/reset/confirm/{uid}/{token}',  # TODO: urls in frontend, POST to back
    'USERNAME_RESET_CONFIRM_URL': 'accounts/reset/confirm/{uid}/{token}',  # TODO: urls in frontend, POST to back
    'SEND_ACTIVATION_EMAIL': False,
    'SEND_CONFIRMATION_EMAIL': False,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': False,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': False,
    'EMAIL': {
        'activation': 'app_accounts.emails.CustomActivationEmail',
        'confirmation': 'app_accounts.emails.CustomConfirmationEmail',
        'password_reset': 'app_accounts.emails.CustomPasswordResetEmail',
        'password_changed_confirmation': 'app_accounts.emails.CustomPasswordChangedConfirmationEmail',
        'username_changed_confirmation': 'app_accounts.emails.CustomUsernameChangedConfirmationEmail',
        'username_reset': 'app_accounts.emails.CustomUsernameResetEmail',
    }
}
