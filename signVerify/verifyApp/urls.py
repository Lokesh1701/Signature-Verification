from django.urls import path, include
from rest_framework import routers

from .views import ModelTrain
from .views import signVerify

router = routers.DefaultRouter()
router.register(r'ModelTrain', ModelTrain, basename="ModelTrain")
router.register(r'signVerify', signVerify, basename="signVerify")

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('', include(router.urls)),
]