from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet, ReviewView, TagsView

router = DefaultRouter()
router.register("product", ProductViewSet)

app_name = "goods"

urlpatterns = [
    path("", include(router.urls)),
    path("product/<int:product_id>/reviews", ReviewView.as_view(), name="review"),
    path("tags", TagsView.as_view(), name="tags"),
]
