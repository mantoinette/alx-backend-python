# chats/pagination.py

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomMessagePagination(PageNumberPagination):
    page_size = 20  # ✅ Required keyword
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,  # ✅ Required keyword
            'pages': self.page.paginator.num_pages,
            'current': self.page.number,
            'results': data
        })
