INSTALLED_APPS = ['djoser']
DJOSER = {
    'LOGIN_FIELD': 'username',
    'TOKEN_MODEL': None,  # needed for JWT
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
    'SERIALIZERS': {
    #     'activation': 'djoser.serializers.ActivationSerializer',
    #     'password_reset': 'djoser.serializers.SendEmailResetSerializer',
    #     'password_reset_confirm': 'djoser.serializers.PasswordResetConfirmSerializer',
    #     'password_reset_confirm_retype': 'djoser.serializers.PasswordResetConfirmRetypeSerializer',
    #     'set_password': 'djoser.serializers.SetPasswordSerializer',
    #     'set_password_retype': 'djoser.serializers.SetPasswordRetypeSerializer',
    #     'set_username': 'djoser.serializers.SetUsernameSerializer',
    #     'set_username_retype': 'djoser.serializers.SetUsernameRetypeSerializer',
    #     'username_reset': 'djoser.serializers.SendEmailResetSerializer',
    #     'username_reset_confirm': 'djoser.serializers.UsernameResetConfirmSerializer',
    #     'username_reset_confirm_retype': 'djoser.serializers.UsernameResetConfirmRetypeSerializer',
    #     'user_create': 'djoser.serializers.UserCreateSerializer',
    #     'user_create_password_retype': 'djoser.serializers.UserCreatePasswordRetypeSerializer',
    #     'user_delete': 'djoser.serializers.UserDeleteSerializer',
    #     'user': 'djoser.serializers.UserSerializer',
    #     'current_user': 'djoser.serializers.UserSerializer',
    #     'token': 'djoser.serializers.TokenSerializer',
    #     'token_create': 'djoser.serializers.TokenCreateSerializer',
    },
    'EMAIL': {
        'activation': 'app_accounts.emails.CustomActivationEmail',
        'confirmation': 'app_accounts.emails.CustomConfirmationEmail',
        'password_reset': 'app_accounts.emails.CustomPasswordResetEmail',
        'password_changed_confirmation': 'app_accounts.emails.CustomPasswordChangedConfirmationEmail',
        'username_changed_confirmation': 'app_accounts.emails.CustomUsernameChangedConfirmationEmail',
        'username_reset': 'app_accounts.emails.CustomUsernameResetEmail',
    },
    'PERMISSIONS': {
        # 'activation': ['rest_framework.permissions.AllowAny'],
        # 'password_reset': ['rest_framework.permissions.AllowAny'],
        # 'password_reset_confirm': ['rest_framework.permissions.AllowAny'],
        # 'set_password': ['rest_framework.permissions.CurrentUserOrAdmin'],
        # 'username_reset': ['rest_framework.permissions.AllowAny'],
        # 'username_reset_confirm': ['rest_framework.permissions.AllowAny'],
        # 'set_username': ['rest_framework.permissions.CurrentUserOrAdmin'],
        # 'user_create': ['rest_framework.permissions.AllowAny'],
        # 'user_delete': ['rest_framework.permissions.CurrentUserOrAdmin'],
        'user_delete': ['rest_framework.permissions.IsAdminUser'],
        # 'user': ['rest_framework.permissions.CurrentUserOrAdmin'],
        # 'user_list': ['rest_framework.permissions.CurrentUserOrAdmin'],
        # 'token_create': ['rest_framework.permissions.AllowAny'],
        # 'token_destroy': ['rest_framework.permissions.IsAuthenticated'],
    }
}
