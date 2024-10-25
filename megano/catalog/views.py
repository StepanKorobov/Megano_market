from typing import List

from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from goods.models import Product

from .models import Category, Sale
from .paginations import CustomPageNumberPagination
from .serializers import CategorySerializer, ProductSerializer, SaleSerializer


class CategoriesView(APIView):
    """
    Класс для получения всех категорий и подкатегорий товаров
    """

    @method_decorator(cache_page(60 * 5))
    def get(self, request: Request) -> Response:
        categories: Category = (
            Category.objects.select_related("image")
            .prefetch_related("subcategories")
            .select_related("image")
        )
        serializer: CategorySerializer = CategorySerializer(categories, many=True)

        return Response(serializer.data)


class ProductListView(generics.ListAPIView):
    """
    Класс для получения товаров по фильтру
    """

    serializer_class = ProductSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        """
        Переопределяем запрос
        """
        # Создаём запрос
        queryset: Product = (
            Product.objects.select_related("category")
            .prefetch_related("reviews", "tags", "images")
            .all()
        )

        # Получаем параметр сортировки
        param_sort: str = self.request.query_params.get("sort")
        # Получаем тип сортировки
        type_sort: str = self.request.query_params.get("sortType")

        # Получаем теги
        tags: List[int | None] = self.request.query_params.getlist("tags[]")

        # Получаем строку для поиска
        search_name: str = self.request.query_params.get("filter[name]")
        # Получаем минимальную цену
        min_price: int = self.request.query_params.get("filter[minPrice]")
        # Получаем максимальную цену
        max_price: int = self.request.query_params.get("filter[maxPrice]")
        # Получаем пункт о бесплатной доставки
        free_delivery: bool = self.request.query_params.get("filter[freeDelivery]")
        # Получаем пункт о наличии товара
        available: bool = self.request.query_params.get("filter[available]")

        # Преобразуем параметр сортировки по популярности в нужный нам
        param_sort: str = "count_reviews" if param_sort == "reviews" else param_sort
        # Преобразуем тип сортировки в нужный нам
        sort_type: str = "-" if type_sort == "dec" else ""
        # Преобразуем доставку в булевое значение
        free_delivery: bool = True if free_delivery == "true" else False
        # Преобразуем наличие в количество (если больше нуля, значит товар в наличии)
        available: int = 0 if available == "true" else -1

        # Запрос со всеми параметрами фильтрации и сортировки
        queryset: Product = (
            queryset.annotate(count_reviews=Count("reviews"))
            .order_by(f"{sort_type}{param_sort}")
            .filter(
                price__range=(min_price, max_price),
                title__icontains=search_name,
                count__gt=available,
            )
        )

        # Если в запросе присутствуют теги, добавляем их в фильтр
        if free_delivery:
            queryset = queryset.filter(freeDelivery=free_delivery)
        if tags:
            queryset = queryset.filter(tags=tuple(tags))

        return queryset


class ProductPopularView(APIView):
    """
    Класс для вывода популярных товаров
    """

    @method_decorator(cache_page(60 * 5))
    def get(self, request):
        products_popular: Product = (
            Product.objects.select_related("category")
            .prefetch_related("reviews", "tags", "images")
            .all()
            .order_by("-rating")[:8]
        )
        serializer: ProductSerializer = ProductSerializer(products_popular, many=True)

        return Response(serializer.data)


class ProductLimitedView(APIView):
    """
    Класс для вывода лимитированных товаров
    """

    @method_decorator(cache_page(60 * 5))
    def get(self, request):
        product_limited: Product = (
            Product.objects.prefetch_related("reviews", "tags", "images")
            .all()
            .filter(limited=True)[:16]
        )
        serializer: ProductSerializer = ProductSerializer(product_limited, many=True)

        return Response(serializer.data)


class SalesView(generics.ListAPIView):
    """
    Класс для вывода скидок
    """

    queryset: Sale = Sale.objects.prefetch_related("product", "images").all()

    serializer_class = SaleSerializer
    pagination_class = CustomPageNumberPagination


class BannersView(APIView):
    """
    Класс для вывода банеров
    """

    @method_decorator(cache_page(60 * 5))
    def get(self, request):
        product_banners: Product = (
            Product.objects.prefetch_related("reviews", "tags", "images")
            .all()
            .filter(banners=True)[:3]
        )
        serializer: ProductSerializer = ProductSerializer(product_banners, many=True)

        return Response(serializer.data)
