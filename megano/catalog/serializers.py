from rest_framework import serializers

from goods.models import Image, Product, Tag

from .models import (
    Category,
    CategoryImage,
    Sale,
    SaleImage,
    SubCategory,
    SubCategoryImage,
)


class SubCategoryImageSerializer(serializers.ModelSerializer):
    """Сериализатор картинок подкатегорий товаров"""

    class Meta:
        model = SubCategoryImage
        fields = ["src", "alt"]


class CategoryImageSerializer(serializers.ModelSerializer):
    """Сериализатор картинок категорий товаров"""

    class Meta:
        model = CategoryImage
        fields = ["src", "alt"]


class SubCategorySerializer(serializers.ModelSerializer):
    """Сериализатор подкатегории товаров"""

    image = SubCategoryImageSerializer()

    class Meta:
        model = SubCategory
        fields = ["title", "image"]


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий товаров"""

    subcategories = SubCategorySerializer(many=True)
    image = CategoryImageSerializer()

    class Meta:
        model = Category
        fields = ["title", "subcategories", "image"]


class SaleImagesSerializer(serializers.ModelSerializer):
    """Сериализатор картинок скидок товаров"""

    class Meta:
        model = SaleImage
        fields = ["src", "alt"]


class SaleSerializer(serializers.ModelSerializer):
    """Сериализатор скидок товаров"""

    images = SaleImagesSerializer(many=True, read_only=True)
    id = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = ["id", "price", "salePrice", "dateFrom", "dateTo", "title", "images"]

    def get_id(self, obj):
        # метод для получения id товара (так как в ответе нам нужен именно он, для перехода на страницу товара)
        return obj.product.pk


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов"""

    class Meta:
        model = Tag
        fields = ["id", "name"]


class ImageSerializer(serializers.ModelSerializer):
    """Сериализатор картинок товаров"""

    class Meta:
        model = Image
        fields = ["src", "alt"]


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор товаров"""

    images = ImageSerializer(many=True, read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    tags = serializers.SlugRelatedField(
        many=True, slug_field="name", queryset=Tag.objects.all()
    )
    reviews = serializers.SerializerMethodField()

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
            "rating",
            "reviews",
        ]

    def get_reviews(self, obj):
        # метод для подсчёта количества отзывов
        return obj.reviews.count()
