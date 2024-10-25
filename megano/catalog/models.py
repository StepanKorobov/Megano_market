from django.db import models


class Sale(models.Model):
    """
    Модель для скидок
    """

    price = models.DecimalField(max_digits=10, decimal_places=2)
    salePrice = models.DecimalField(max_digits=10, decimal_places=2)
    dateFrom = models.DateField()
    dateTo = models.DateField()
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"Sale (PK={self.pk} | Title={self.title})"


class SaleImage(models.Model):
    """
    Модель для картинок скидок
    """

    sale = models.ForeignKey(Sale, related_name="images", on_delete=models.CASCADE)
    src = models.ImageField(upload_to="sales/images")
    alt = models.CharField(max_length=100)

    def __str__(self):
        return f"Image (PK={self.pk}) | alt={self.alt}"


class Category(models.Model):
    """
    Модель для категорий товаров
    """

    title = models.CharField(max_length=100)

    def __str__(self):
        return f"Category (PK={self.pk} | Tite={self.title})"


class SubCategory(models.Model):
    """
    Модель для подкатегорий
    """

    category = models.ForeignKey(
        Category, related_name="subcategories", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"SubCategory (PK={self.pk} | Tite={self.title})"


class CategoryImage(models.Model):
    """
    Модель для хранения картинок категорий
    """

    category = models.OneToOneField(
        Category, related_name="image", on_delete=models.CASCADE
    )
    src = models.ImageField(upload_to="category/images")
    alt = models.CharField(max_length=100)

    def __str__(self):
        return f"Category Image (PK={self.pk} | alt={self.alt})"


class SubCategoryImage(models.Model):
    """
    Модель для хранения картинок подкатегорий
    """

    subcategories = models.OneToOneField(
        SubCategory, related_name="image", on_delete=models.CASCADE
    )
    src = models.ImageField(upload_to="subcategories/images")
    alt = models.CharField(max_length=100)

    def __str__(self):
        return f"Subcategory Image (PK={self.pk} | alt={self.alt})"
