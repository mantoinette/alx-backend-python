import time
import threading
from collections import deque
from django.conf import settings
from django.http import JsonResponse


class OffensiveLanguageMiddleware:
  
    def __init__(self, get_response):
        self.get_response = get_response
        self.limit = getattr(settings, "MESSAGE_RATE_LIMIT", 5)
        self.window = getattr(settings, "MESSAGE_RATE_WINDOW", 60)
        self._requests = {}
        self._lock = threading.Lock()

    def _get_client_ip(self, request):
        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        if xff:
            return xff.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "")

    def _prune_old(self, dq, now):
        cutoff = now - self.window
        while dq and dq[0] <= cutoff:
            dq.popleft()

    def __call__(self, request):
        if request.method == "POST":
            ip = self._get_client_ip(request)
            now = time.time()

            with self._lock:
                dq = self._requests.get(ip)
                if dq is None:
                    dq = deque()
                    self._requests[ip] = dq

                self._prune_old(dq, now)

                if len(dq) >= self.limit:
                    retry_after = int(self.window - (now - dq[0])) if dq else self.window
                    payload = {
                        "error": "Too many messages. Please wait before sending more.",
                        "retry_after_seconds": retry_after,
                    }
                    resp = JsonResponse(payload, status=429)
                    resp["Retry-After"] = str(retry_after)
                    return resp

                dq.append(now)

        return self.get_response(request)
