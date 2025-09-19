"""
OffensiveLanguageMiddleware

Middleware that tracks the number of POST requests (chat messages) sent by each IP
and implements a time-based limit (default: 5 messages per 60 seconds). If a user
exceeds the limit, further messages are blocked and an error is returned.

To use this middleware:
Add the following line to MIDDLEWARE in your Django project's settings.py:
    'chats.middleware.OffensiveLanguageMiddleware'

Optional configuration in settings.py:
    MESSAGE_RATE_LIMIT = 5        # number of messages allowed per window
    MESSAGE_RATE_WINDOW = 60      # time window in seconds
"""

import time
import threading
from collections import deque

from django.conf import settings
from django.http import JsonResponse


class OffensiveLanguageMiddleware:
    """
    Middleware class that rate-limits POST requests per IP address.
    """

    def __init__(self, get_response):
        # Standard Django middleware initialization
        self.get_response = get_response

        # Get rate limit settings from Django settings, with defaults
        self.limit = getattr(settings, "MESSAGE_RATE_LIMIT", 5)
        self.window = getattr(settings, "MESSAGE_RATE_WINDOW", 60)

        # Store recent request timestamps per IP
        self._requests = {}  # ip -> deque([timestamps])
        self._lock = threading.Lock()  # to handle concurrency

    def _get_client_ip(self, request):
        """
        Retrieve the client's IP address, checking X-Forwarded-For if behind a proxy.
        """
        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        if xff:
            return xff.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "")

    def _prune_old(self, dq, now):
        """
        Remove timestamps older than the window from the deque.
        """
        cutoff = now - self.window
        while dq and dq[0] <= cutoff:
            dq.popleft()

    def __call__(self, request):
        """
        Process each request:
        - Count POST requests as messages
        - Block if the number of messages exceeds the limit within the window
        """
        if request.method == "POST":
            ip = self._get_client_ip(request)
            now = time.time()

            with self._lock:
                dq = self._requests.get(ip)
                if dq is None:
                    dq = deque()
                    self._requests[ip] = dq

                # Remove timestamps outside the time window
                self._prune_old(dq, now)

                # If the user has exceeded the limit, block the request
                if len(dq) >= self.limit:
                    retry_after = int(self.window - (now - dq[0])) if dq else self.window
                    payload = {
                        "error": "Too many messages. Please wait before sending more.",
                        "retry_after_seconds": retry_after,
                    }
                    resp = JsonResponse(payload, status=429)
                    resp["Retry-After"] = str(retry_after)
                    return resp

                # Otherwise, record this request timestamp
                dq.append(now)

        # Continue normal request processing
        return self.get_response(request)
