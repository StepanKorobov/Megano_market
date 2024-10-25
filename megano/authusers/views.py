import json
from typing import Dict

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from basket.models import Basket
from profiles.models import Profile


def basket_transfer(request: Request, user: User) -> None:
    """
    Класс для переноса корзины (при логине и регистрации)

    :param request: Запрос
    :type request: Request
    :param user: Пользователь
    :type user: User
    :return:
    :rtype: None
    """
    # Получаем ключ сессии
    session_key: int = request.session.session_key
    # проверяем существует ли корзина у пользователя
    basket_user_exist: bool = Basket.objects.filter(user=user).exists()

    # Корзины у пользователя нет
    if not basket_user_exist:
        # Получаем корзину по ключу сессии
        basket = Basket.objects.filter(session_key=session_key)
        # В цикле добавляем пользователя
        for i_basket in basket:
            i_basket.user = user
            i_basket.session_key = None
            i_basket.save()
    # Корзина у пользователя есть
    else:
        # Получаем корзину по ключу сессии
        basket = Basket.objects.filter(session_key=session_key)
        # Удаляем корзину
        for i_basket in basket:
            i_basket.delete()


class SignInView(APIView):
    """
    Класс для авторизации пользователей.
    """

    def post(self, request: Request) -> Response:
        """
        Метод для авторизации пользователей
        """

        # Получаем данные из запроса и преобразуем их в json
        user_data: Dict = json.loads(request.body)
        # Получаем логин
        username: str = user_data.get("username")
        # Получаем пароль
        password: str = user_data.get("password")

        # Проходим аутентификацию
        user: User = authenticate(request=request, username=username, password=password)

        # Проверяем есть ли такой пользователь
        if user:
            # Переносим корзину
            basket_transfer(request=request, user=user)

            # логинимся
            login(request=request, user=user)

            # Успешный вход
            return Response(status=status.HTTP_200_OK)

        # Непредвиденная ошибка
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignUpView(APIView):
    """
    Класс для регистрации пользователей.
    """

    def post(self, request: Request) -> JsonResponse:
        """
        Метод для регистрации пользователей.
        """

        try:
            # Получаем данные из запроса и преобразуем их в json
            user_data: Dict = json.loads(request.body)
            # Получаем логин
            username: str = user_data.get("username")
            # Получаем пароль
            password: str = user_data.get("password")
            # Получаем имя пользователя
            first_name: str = user_data.get("name", "")

            # Проверяем наличие логина и пароля
            if not username or not password:
                # Не все поля были заполнены
                return JsonResponse(
                    {"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST
                )
            # Проверяем наличие пользователя с данным логином
            if User.objects.filter(username=username).exists():
                # Пользователь не уникален
                return JsonResponse(
                    {"error": "Username already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Если все данные заполнены и пользователь уникален, то создаём нового
            user: User = User.objects.create_user(
                username=username, password=password, first_name=first_name
            )
            # Создаём пользователя
            Profile.objects.create(user=user)
            # Переносим корзину
            basket_transfer(request=request, user=user)
            # Логинимся
            login(request, user)

            # Пользователь создан
            return JsonResponse(
                {"message": "User created successfully"}, status=status.HTTP_200_OK
            )

        except Exception as e:
            # Непредвиденная ошибка
            return JsonResponse(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SignOutView(APIView):
    """
    Класс для разлогинивания пользователей.
    """

    def post(self, request: Request) -> Response:
        """
        Метод для разлогинивания пользователей.
        """

        # Разлогиниваемся
        logout(request)

        # Успешно разлогинились
        return Response(status=status.HTTP_200_OK)
