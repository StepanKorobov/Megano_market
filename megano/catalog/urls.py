from django.urls import path

from .views import (
    BannersView,
    CategoriesView,
    ProductLimitedView,
    ProductListView,
    ProductPopularView,
    SalesView,
)

app_name = "catalog"

urlpatterns = [
    path("catalog", ProductListView.as_view(), name="catalog"),
    path("categories", CategoriesView.as_view(), name="categories"),
    path("products/popular", ProductPopularView.as_view(), name="product-popular"),
    path("products/limited", ProductLimitedView.as_view(), name="product-limited"),
    path("sales", SalesView.as_view(), name="sales"),
    path("banners", BannersView.as_view(), name="banners"),
]
