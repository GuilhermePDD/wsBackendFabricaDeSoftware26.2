from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import GovernadorViewSet, GastoViewSet, EstadosInfoView

router = DefaultRouter()
router.register("governadores", GovernadorViewSet)
router.register("gastos", GastoViewSet)

urlpatterns = router.urls + [
    path("estados/", EstadosInfoView.as_view(), name="estados-info"),
]
