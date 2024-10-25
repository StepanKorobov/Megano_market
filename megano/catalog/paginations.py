from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    """
    Класс для кастомной пагинации
    """

    # Определяем количество объектов на странице
    page_size = 8
    # Определяем параметр запроса в котором указанна требуемая страница
    page_query_param = "currentPage"

    def get_paginated_response(self, data):
        # Переопределяем метод для ответа
        return Response(
            {
                "items": data,
                "currentPage": self.page.number,
                "lastPage": self.page.paginator.num_pages,
            }
        )
