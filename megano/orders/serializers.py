from rest_framework import serializers

from orders.models import Order, OrdersData


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор Товаров в заказе
    """

    id = serializers.IntegerField(source="product.id")
    category = serializers.IntegerField(source="product.category.id")
    price = serializers.DecimalField(
        source="product.price", max_digits=10, decimal_places=2
    )
    # date = serializers.DateTimeField(source='date_added')
    date = serializers.DateTimeField(source="product.date")
    title = serializers.CharField(source="product.title")
    description = serializers.CharField(source="product.description")
    freeDelivery = serializers.BooleanField(source="product.freeDelivery")
    images = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    reviews = serializers.IntegerField(source="product.reviews.count")
    rating = serializers.FloatField(source="product.rating")

    class Meta:
        model = Order
        fields = [
            "id",
            "category",
            "price",
            "date",
            "count",
            "title",
            "description",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "rating",
        ]

    def get_images(self, obj):
        return [
            {"src": image.src.url, "alt": image.alt}
            for image in obj.product.images.all()
        ]

    def get_tags(self, obj):
        return [{"id": tag.id, "name": tag.name} for tag in obj.product.tags.all()]


class OrderDataSerializer(serializers.ModelSerializer):
    """
    Сериализатор заказов
    """

    # products = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = OrdersData
        fields = [
            "id",
            "createdAt",
            "fullName",
            "email",
            "phone",
            "deliveryType",
            "paymentType",
            "totalCost",
            "status",
            "city",
            "address",
            "products",
        ]
