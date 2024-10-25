from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import OrdersData

from .models import Payment
from .serializers import PaymentSerializer


class PaymentAPIView(APIView):
    """
    Класс для оплаты
    """

    def post(self, request: Request, pk) -> Response:
        """
        Метод для оплаты
        """

        try:
            payment = Payment.objects.get(pk=pk)
            # Проверяем данные из запроса
            serializer = PaymentSerializer(data=request.data)

            # Если данные валидны, обновляем значения
            if serializer.is_valid():
                # Получаем данные из запроса
                data = request.data

                # Обновляем номер
                payment.number = data["number"]
                # Обновляем ФИО
                payment.name = data["name"]
                # Обновляем месяц банковской карты
                payment.month = data["month"]
                # Обновляем год банковской карты
                payment.year = data["year"]
                # Обновляем код банковской карты
                payment.code = data["code"]
                # Сохраняем данные
                payment.save()

                # получаем заказ
                order = OrdersData.objects.get(pk=pk)
                # Обновляем статус заказа
                order.status = "accepted"
                # Сохраняем
                order.save()

                # Возвращаем код 200
                return Response(status=status.HTTP_200_OK)

            # Если данные не валидны, возвращаем ошибку
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except payment.DoesNotExist:
            # Если оплата не найдена
            return Response(status=status.HTTP_400_BAD_REQUEST)
