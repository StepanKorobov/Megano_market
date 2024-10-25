from django.contrib import admin
from fieldsets_with_inlines import FieldsetsInlineMixin

from .models import Image, Product, Review, Specification, Tag


class TagsInLine(admin.TabularInline):
    model = Product.tags.through


class SpecificationInLine(admin.TabularInline):
    model = Specification


class ImageInLine(admin.StackedInline):
    model = Image


@admin.register(Tag)
class TagsAdmin(FieldsetsInlineMixin, admin.ModelAdmin):
    """
    Админка тегов
    """

    list_display = ("pk", "name")
    list_display_links = ("pk", "name")
    ordering = ("pk", "name")
    search_fields = ("name",)
    list_filter = ("name",)

    fieldsets_with_inlines = [
        (
            None,
            {
                "fields": ("name",),
            },
        ),
        TagsInLine,
    ]


@admin.register(Specification)
class SpecificationsAdmin(admin.ModelAdmin):
    """
    Админка спецификации (характеристики) товаров
    """

    list_display = ("pk", "name", "value")
    list_display_links = ("pk", "name")
    ordering = ("pk", "name")
    search_fields = ("name", "value")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Админка отзывов
    """

    list_display = ("pk", "author", "email", "short_text", "rate", "date")
    list_display_links = ("pk", "author")
    ordering = ("pk", "author")
    search_fields = ("author", "email", "short_text")
    list_filter = ("author", "rate", "date")

    fieldsets = [
        (None, {"fields": ("author", "email", "text", "rate")}),
        (
            "Product",
            {
                "fields": ("product",),
            },
        ),
    ]

    def short_text(self, obj: Review):
        if len(obj.text) < 48:
            return obj.text

        return obj.text[:48] + "..."


@admin.register(Product)
class ProductsAdmin(FieldsetsInlineMixin, admin.ModelAdmin):
    """
    Админка товаров
    """

    list_display = (
        "pk",
        "title",
        "price",
        "count",
        "description",
        "freeDelivery",
        "limited",
        "rating",
        "date",
        "sales",
    )
    list_display_links = ("pk", "title")
    ordering = ("pk", "title")
    search_fields = ("title", "description")
    list_filter = ("freeDelivery", "limited", "rating")

    fieldsets_with_inlines = [
        (
            "Exclusive",
            {
                "fields": ("limited", "banners", "freeDelivery"),
                "classes": ("collapse",),
            },
        ),
        (
            "Sales",
            {
                "fields": ("sales",),
                "classes": ("collapse",),
            },
        ),
        (
            None,
            {
                "fields": (
                    "title",
                    "price",
                    "count",
                    "description",
                    "fullDescription",
                )
            },
        ),
        (
            "Relation",
            {
                "fields": (
                    "category",
                    "tags",
                ),
            },
        ),
        SpecificationInLine,
        ImageInLine,
    ]
