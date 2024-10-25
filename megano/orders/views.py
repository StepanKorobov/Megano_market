from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from basket.models import Basket
from payment.models import Payment
from profiles.models import Profile

from .models import OrdersData
from .serializers import OrderDataSerializer


class OrderApiView(APIView):
    """
    Клас для создания нового заказа, и получения истории заказов
    """

    def get(self, request):
        """
        Метод для получения истории заказов
        """
        if request.user.is_authenticated:
            # Получаем полтзователя
            user = request.user
            # Получаем заказы
            orders = OrdersData.objects.filter(user=user)
            # Сериализуем данные
            serializer = OrderDataSerializer(orders, many=True)
            # Возвращем список заказов
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Если пользователь не авторизован
        return Response(
            {"detail": "No authorized"}, status=status.HTTP_401_UNAUTHORIZED
        )

    def post(self, request: Request) -> Response:
        """
        Метод для создания нового заказа
        """
        if request.user.is_authenticated:
            # Получаем пользователя
            user: User = request.user
            # Данные о товарах в заказе
            request_data = request.data

            # Получаем профиль
            profile = Profile.objects.get(user=user)

            # Полное имя
            full_name = profile.fullName
            # Телефон
            phone = profile.phone
            # Почта
            email = profile.email

            # Обновляем заказ
            order_data = OrdersData(
                user=user,
                products=request_data,
                status="created",
                full_name=full_name if full_name else "",
                phone=phone if phone else "",
                email=email if email else "",
            )
            # Сохраняем
            order_data.save()
            # Создаём оплату
            payment = Payment()
            # Сохраняем
            payment.save()

            return Response({"orderId": order_data.pk}, status=status.HTTP_200_OK)

        # Если пользователь не авторизован
        return Response(
            {"detail": "No authorized"}, status=status.HTTP_401_UNAUTHORIZED
        )


class OrderViewSet(APIView):
    """
    Класс для работы с заказами
    """

    def get(self, request: Request, pk) -> Response:
        """
        Метод для получения конкретного заказа
        """
        # Проверяем существует ли данный заказ
        try:
            order = OrdersData.objects.get(id=pk)
        except OrdersData.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # order = OrdersData.objects.prefetch_related('products').filter(pk=pk)
        # Сериализуем нужный заказ
        serializer = OrderDataSerializer(order)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request, pk) -> Response:
        """
        Метод для обновления конкретного заказа
        """
        serializer = OrderDataSerializer(data=request.data)

        # Проверяем данные из запроса
        if serializer.is_valid():
            data = request.data
            # Получаем заказ по id
            order = OrdersData.objects.get(pk=pk)
            # Обновляем ФИО
            order.fullName = data["fullName"]
            # Обновляем email
            order.email = data["email"]
            # Обновляем телефон
            order.phone = data["phone"]
            # Обновляем стоимость всего заказа
            order.totalCost = data["basketCount"]["price"]
            # Обновляем статус заказа
            order.status = "payment"
            # Обновляем город
            order.city = data["city"]
            # Обновляем адрес
            order.address = data["address"]

            # Сохраняем обновления
            order.save()

            # Получаем пользователя
            user = request.user
            # Получаем корзину
            basket = Basket.objects.filter(user=user)
            # Удаляем все элементы, так как они переходят в заказ
            for i_basket in basket:
                i_basket.delete()

            # Возвращаем id ордера
            return Response({"orderId": pk}, status=status.HTTP_200_OK)

        # Ошибки валидации
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
