from utils.middleware_requests_url_access import request_validate_url_access
from utils.middleware_requests_and_blocks import request_validate_connection

class CustomMiddleware(object):
    def __init__(self, get_response):
        """
        One-time configuration and initialisation.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Code to be executed for each request before the view (and later
        middleware) are called.
        """
        # response Claim id messages description:
        # [ Claim id: 0/0 ] = request_validate_url_access/anonymous request
        # [ Claim id: 0/+1 ] = request_validate_url_access/user request
        # [ Claim id: +1/0 ] = request_validate_connection per ban id/anonymous request
        # [ Claim id: +1/+1 ] = request_validate_connection per ban id/user request

        # Check request URL permission for User/Anonymous
        response = request_validate_url_access(self, request)
        if response:
            return response
        # save request history from user and anonymous.
        # Link them with parent_id.
        # Add ban module from models app_accounts
        response = request_validate_connection(self, request)
        if response:
            return response

        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Called just before Django calls the view.
        """
        return None

    def process_exception(self, request, exception):
        """
        Called when a view raises an exception.
        """
        return None

    def process_template_response(self, request, response):
        """
        Called just after the view has finished executing.
        """
        return response
