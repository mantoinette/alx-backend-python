import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='user_requests.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        logging.info(f"{datetime.now()} - User: {user} - Path: {request.path}")

        response = self.get_response(request)
        return response
