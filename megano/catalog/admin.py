from django.contrib import admin
from nested_admin import NestedModelAdmin, NestedStackedInline

from .models import (
    Category,
    CategoryImage,
    Sale,
    SaleImage,
    SubCategory,
    SubCategoryImage,
)


class SaleImageInline(admin.StackedInline):
    model = SaleImage
    extra = 1


class CategoryImageInline(NestedStackedInline):
    model = CategoryImage


class SubCategoryImageInline(NestedStackedInline):
    model = SubCategoryImage


class SubCategoryInline(NestedStackedInline):
    model = SubCategory
    extra = 1
    inlines = [SubCategoryImageInline]


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    """
    Админка скидок
    """

    list_display = ("id", "title", "price", "salePrice", "dateFrom", "dateTo")
    list_display_links = ("id", "title")
    ordering = ("id",)
    search_fields = ("title",)

    fieldsets = [
        (None, {"fields": ("title", "price", "salePrice", "dateFrom", "dateTo")})
    ]

    inlines = [SaleImageInline]


@admin.register(Category)
class CategoryAdmin(NestedModelAdmin):
    """
    Админка категорий
    """

    list_display = ("id", "title")
    list_display_links = ("id", "title")
    search_fields = ("title",)

    inlines = [CategoryImageInline, SubCategoryInline]


@admin.register(SubCategory)
class SubCategoryAdmin(NestedModelAdmin):
    """
    Админка подкатегорий
    """

    list_display = ("id", "title")
    list_display_links = ("id", "title")
    search_fields = ("title",)

    inlines = [SubCategoryImageInline]
