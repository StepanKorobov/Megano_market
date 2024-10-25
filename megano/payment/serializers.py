import datetime

from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для оплаты
    """

    class Meta:
        model = Payment
        fields = ["number", "name", "month", "year", "code"]

    def validate_number(self, value):
        """
        Валидатор для номера карты
        """
        if len(str(value)) != 16:
            raise serializers.ValidationError(
                "The card number must consist of 16 digits."
            )

        return value

    def validate_month(self, value):
        """
        Валидатор на проверку месяца
        """
        if not 0 < value < 13:
            raise serializers.ValidationError("month number must be between 1 and 12.")

        return value

    def validate_year(self, value):
        """
        Валидатор на проверку года
        """
        today = datetime.date.today()
        current_year = today.year

        if not 2009 < value <= current_year:
            raise serializers.ValidationError(
                f"year number must be between 2009 and {current_year}."
            )

        return value

    def validate_code(self, value):
        """
        Валидатор на проверку кода
        """
        if not 99 < value < 1000:
            raise serializers.ValidationError("the code must consist of 3 digits.")

        return value
