from rest_framework import serializers

from catalog.models import Category

from .models import Image, Product, Review, Specification, Tag


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов"""

    class Meta:
        model = Tag
        fields = ["id", "name"]


class SpecificationSerializer(serializers.ModelSerializer):
    """Сериализатор спецификации (характеристик) товара"""

    class Meta:
        model = Specification
        fields = ["name", "value"]


class ImageSerializer(serializers.ModelSerializer):
    """Сериализатор картинок товара"""

    class Meta:
        model = Image
        fields = ["src", "alt"]


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов на товар"""

    class Meta:
        model = Review
        fields = ["author", "email", "text", "rate", "date"]

        # Не работает
        # def create(self, validated_data):
        #     product = self.context.get('product')
        #
        #     return Review.objects.create(product=product.id, **validated_data)


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор товароа"""

    images = ImageSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    # tags = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Tag.objects.all())
    tags = TagSerializer(many=True, read_only=True)
    specifications = SpecificationSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "fullDescription",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "specifications",
            "rating",
        ]
