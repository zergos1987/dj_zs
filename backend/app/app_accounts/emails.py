from djoser import email as djoser_email


class CustomActivationEmail(djoser_email.ActivationEmail):
    template_name = "app_accounts/email/activation.html"


class CustomConfirmationEmail(djoser_email.ConfirmationEmail):
    template_name = "app_accounts/email/confirmation.html"


class CustomPasswordResetEmail(djoser_email.PasswordResetEmail):
    template_name = "app_accounts/email/password_reset.html"


class CustomPasswordChangedConfirmationEmail(djoser_email.PasswordChangedConfirmationEmail):
    template_name = "app_accounts/email/password_changed_confirmation.html"


class CustomUsernameChangedConfirmationEmail(djoser_email.UsernameChangedConfirmationEmail):
    template_name = "app_accounts/email/username_changed_confirmation.html"


class CustomUsernameResetEmail(djoser_email.UsernameResetEmail):
    template_name = "app_accounts/email/username_reset.html"
