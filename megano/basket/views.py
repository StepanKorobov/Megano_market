from django.contrib.auth.models import User
from django.db.models import Prefetch
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from goods.models import Product

from .models import Basket
from .serializers import BasketSerializer


def get_basket(request: Request) -> Basket:
    """
    Функция для получения корзины
    в зависимости авторизирован пользователь или нет
    """
    queryset = Basket.objects.prefetch_related(
        Prefetch(
            lookup="product",
            queryset=Product.objects.prefetch_related(
                "images", "tags", "category", "reviews"
            ),
        )
    ).all()

    # если пользователь авторизирован, то получаем его корзину
    if request.user.is_authenticated:
        user: User = request.user
        basket: Basket = queryset.filter(user_id=user)
    # если пользователь авторизирован, то получаем ключ сессии
    else:
        session_key: str = request.session.session_key
        basket: Basket = queryset.filter(session_key=session_key)

    return basket


class BasketApiView(APIView):
    """
    Класс для корзины заказов
    """

    def get(self, request: Request) -> Response:
        """
        Метод для получения заказов в корзине
        """

        # Получаем корзину
        basket: Basket = get_basket(request)

        # Сериализуем данные
        serializer: BasketSerializer = BasketSerializer(basket, many=True)

        # Возвращаем данные
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """
        Метод для добавления заказов в корзину
        """

        # ID продукта, который будем добавлять
        product_id: int = request.data.get("id")
        # Получаем количество продукта
        count: int = request.data.get("count")

        # Если пользователь не авторизован
        if not request.user.is_authenticated:
            # Получаем ключ сессии
            session_key: int = request.session.session_key
            # Если ключа сессии нет
            if not session_key:
                # Устанавливаем ключ сессии
                request.session.create()
                # Получаем ключ сессии
                session_key: int = request.session.session_key

        try:
            # Получаем продукт
            product: Product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            # Если не найден, то возвращаем 404
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Если пользователь авторизован
        if request.user.is_authenticated:
            # Получаем пользователя
            user: User = request.user
            # Получаем корзину с нужным продуктом
            basket, created = Basket.objects.get_or_create(
                user=user, product=product, defaults={"count": count}
            )
        # Если пользователь не авторизован
        else:
            # Получаем корзину с нужным продуктом
            basket, created = Basket.objects.get_or_create(
                session_key=session_key, product=product, defaults={"count": count}
            )

        # Если корзина уже создана
        if not created:
            # Добавляем количество продукта
            basket.count += count
            # Сохраняем
            basket.save()

        # Получаем корзину с товарами, для ответа
        basket = get_basket(request)
        # Сериализуем данные
        serializer = BasketSerializer(basket, many=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request: Request) -> Response:
        """
        Метод для удаления товаров из корзины
        """

        # ID продукта, который будем добавлять
        product_id = request.data.get("id")
        # Получаем количество продукта
        count = request.data.get("count")
        # Получаем ключ сессии
        session_key = request.session.session_key

        try:
            # Если пользователь авторизован
            if request.user.is_authenticated:
                # Получаем корзину с продуктом по пользователю
                basket = Basket.objects.get(user=request.user, product=product_id)
            # Если пользователь не авторизован
            else:
                # Получаем корзину с продуктом по ключу сессии
                basket = Basket.objects.get(session_key=session_key, product=product_id)
        except Basket.DoesNotExist:
            # если корзина с продуктом не найдены, возвращаем 404
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Если количество товаров в корзине больше чем нужно удалить
        if basket.count > count:
            # Убавляем количество
            basket.count -= count
            # Сохраняем
            basket.save()
        # Иначе
        else:
            # удаляем корзину с продуктом
            basket.delete()

        # Получаем корзину для ответа
        basket = get_basket(request)
        # Сериализуем данные
        serializer = BasketSerializer(basket, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
