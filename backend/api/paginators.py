
from rest_framework.pagination import PageNumberPagination


class LimitPageNumberPagination(PageNumberPagination):
    """
    Cтандарный пагинатор с лимитом выводимых страниц
    URL: http://127.0.0.1:8000/api/users/subscriptions/?limit=6
    """
    page_size_query_param = 'limit'
