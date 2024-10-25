from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Avatar, Profile
from .serializers import AvatarSerializer, PasswordSerializer, ProfileSerializer


class ProfileView(APIView):
    """
    Класс для получения и обновления профиля пользователя
    """

    def get(self, request: Request) -> Response:
        """
        Метод для получения профиля пользователя
        """

        try:
            # Получаем дынные из запроса
            profile: Profile = request.user.profile
            # Проверяем данные
            serializer: ProfileSerializer = ProfileSerializer(profile)

            # Возвращаем профиль
            return Response(serializer.data)

        except Profile.DoesNotExist:
            # Профиль не найден
            return Response(
                {"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request: Request) -> Response:
        """
        Метод для обновления профиля
        """

        try:
            # Получаем дынные из запроса
            profile: Profile = request.user.profile
            # Проверяем данные
            serializer: ProfileSerializer = ProfileSerializer(
                profile, data=request.data, partial=True
            )

            # Если данные валидны
            if serializer.is_valid():
                # Обновляем профиль
                serializer.save()

                # Успешное обновление профиля
                return Response(serializer.data, status=status.HTTP_200_OK)

            # Данные не прошли валидацию
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Profile.DoesNotExist:
            # Профиль не найден
            return Response(
                {"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND
            )


class ProfileUpdatePasswordView(APIView):
    """
    Класс для обновления пароля пользователя
    """

    def post(self, request: Request) -> Response:
        """
        Метод для обновления пароля пользователя
        """

        try:
            # Проверяем наличие профиля
            profile: Profile = request.user.profile
            # Проверяем данные из запроса
            serializer: PasswordSerializer = PasswordSerializer(
                data=request.data, context={"request": request}
            )

            # Если данные валидны
            if serializer.is_valid():
                # Обновляем пароль
                serializer.save()

                # Успешное обновление пароля
                return Response(serializer.data, status=status.HTTP_200_OK)

            # Ошибки валидации
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Profile.DoesNotExist:
            # Профиль не найден
            return Response(
                {"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND
            )


class ProfileUpdateAvatarView(APIView):
    """
    Класс для обновления аватара пользователя
    """

    def post(self, request: Request) -> Response:
        """
        Метод для обновления аватара пользователя
        """

        try:
            # Проверяем наличие профиля
            profile, created = Profile.objects.get_or_create(user=request.user)
            # Если 'avatar' есть в файлах
            if "avatar" in request.FILES:
                # Проверяем наличие аватара у пользователя
                if hasattr(profile, "avatar"):
                    # получаем аватар
                    avatar: Avatar = profile.avatar
                    # обновляем путь к файлу
                    avatar.src = request.FILES["avatar"]
                    # Сохраняем
                    avatar.save()
                else:
                    # Создаём новый аватар у пользователя
                    avatar: Avatar = Avatar.objects.create(
                        profile=profile, src=request.FILES["avatar"]
                    )

                # Проверяем данные и сохраняем аватар в локальных файлах
                serializer: AvatarSerializer = AvatarSerializer(avatar)

                # Аватар успешно обновлён
                return Response(serializer.data, status=status.HTTP_200_OK)

            else:
                # Файл с аватаром не был отправлен
                return Response(
                    {"detail": "No file provided."}, status=status.HTTP_400_BAD_REQUEST
                )

        except Profile.DoesNotExist:
            # Профиль не найден
            return Response(
                {"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND
            )
