from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Review, Tag
from .serializers import ProductSerializer, ReviewSerializer, TagSerializer


class TagsView(APIView):
    """
    Класс для получения всех тегов
    """

    @method_decorator(cache_page(60 * 1))
    def get(self, request):
        # Получаем все теги
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)

        # Возвращаем теги
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    """
    Класс для получения информации о продукте
    """

    queryset = (
        Product.objects.select_related("category", "sales")
        .prefetch_related("tags")
        .all()
    )
    serializer_class = ProductSerializer


class ReviewView(APIView):
    """
    Класс для публикации отзыва
    """

    def post(self, request, product_id):
        # Проверяем авторизацию
        if request.user.is_authenticated:
            try:
                # Ищем товар
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                # В случе, если товар не найден
                return Response(status=status.HTTP_404_NOT_FOUND)

            # Проверяем данные
            serializer = ReviewSerializer(
                data=request.data, context={"product": product}
            )

            # Если данные валидны
            if serializer.is_valid():
                # Переопределения метода create в сериализаторе не работает
                # Создаем отзыв
                Review(**serializer.data, product=product).save()

                # Получаем список отзывов для ответа
                review = Review.objects.filter(product=product)
                serializer = ReviewSerializer(review, many=True)
                # Возвращаем код 200
                return Response(serializer.data, status=status.HTTP_200_OK)

            # Если данные не валидны возвращаем код 400
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Если пользователь не авторизован
        return Response(
            {"detail": "No authorized"}, status=status.HTTP_401_UNAUTHORIZED
        )
