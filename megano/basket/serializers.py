from rest_framework import serializers

from .models import Basket


class BasketSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="product.id")
    category = serializers.IntegerField(source="product.category.id")
    price = serializers.DecimalField(
        source="product.price", max_digits=10, decimal_places=2
    )
    date = serializers.DateTimeField(source="date_added")
    title = serializers.CharField(source="product.title")
    description = serializers.CharField(source="product.description")
    freeDelivery = serializers.BooleanField(source="product.freeDelivery")
    images = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    reviews = serializers.IntegerField(source="product.reviews.count")
    rating = serializers.FloatField(source="product.rating")

    class Meta:
        model = Basket
        fields = [
            "id",
            "category",
            "price",
            "count",
            "date",
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
