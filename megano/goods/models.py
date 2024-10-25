from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from catalog.models import Category, Sale


def product_images_directory_path(instance: "Images", filename: str) -> str:
    """
    Путь до директории с фотографиями товаров
    """
    return "goods/product_{pk}/images/{filename}".format(
        pk=instance.product.pk,
        filename=filename,
    )


class Tag(models.Model):
    """
    Модель тегов
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        return f"Tag (PK={self.pk} | Tag={self.name})"


class Product(models.Model):
    """
    Модель товаров
    """

    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    count = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    fullDescription = models.TextField()
    freeDelivery = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name="products", blank=True)
    rating = models.FloatField(default=0)
    limited = models.BooleanField(default=False)
    sales = models.OneToOneField(
        Sale, related_name="product", on_delete=models.CASCADE, null=True, blank=True
    )
    banners = models.BooleanField(default=False)

    def calculate_rating(self):
        """
        Метод для расчёта рейтинга товара
        """
        reviews = self.reviews.all()

        # Если отзывы на товар есть
        if reviews.exists():
            # Высчитываем среднюю оценку
            total_rating = sum(i_reviews.rate for i_reviews in reviews)
            average_rating = total_rating / reviews.count()

            return average_rating

        return 0

    def __str__(self):
        return f"Product (PK={self.pk} | Title={self.title})"


class Image(models.Model):
    """
    Модель картинок товаров
    """

    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )
    src = models.ImageField(upload_to=product_images_directory_path)
    alt = models.CharField(max_length=100)

    def __str__(self):
        return f"Image (PK={self.pk} | alt={self.alt})"


class Review(models.Model):
    """
    Модель отзывов
    """

    product = models.ForeignKey(
        Product, related_name="reviews", on_delete=models.CASCADE
    )
    author = models.CharField(max_length=100)
    email = models.EmailField()
    text = models.TextField()
    rate = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review (PK={self.pk} | Author={self.author})"


class Specification(models.Model):
    """
    Модель спецификации (характеристик) товара
    """

    product = models.ForeignKey(
        Product, related_name="specifications", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"Spec (PK={self.pk} | Name={self.name})"


@receiver(post_save, sender=Review)
def update_product_rating(sender, instance, **kwargs):
    """
    Функция-сигнал для обновления рейтинга товара при публикации нового отзыва
    """
    product = instance.product
    product.rating = product.calculate_rating()
    product.save()
