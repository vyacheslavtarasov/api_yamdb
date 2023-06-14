from django.urls import include, path
from rest_framework import routers

from api.views import ReviewsViewSet


app_name = "api"

router = routers.DefaultRouter(trailing_slash=True)
router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewsViewSet, basename="reviews"
)

urlpatterns = [
    path("v1/", include(router.urls)),

]