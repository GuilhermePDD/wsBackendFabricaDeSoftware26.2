from rest_framework.routers import DefaultRouter

from .views import GovernadorViewSet, GastoViewSet

router = DefaultRouter()
router.register("governadores", GovernadorViewSet)
router.register("gastos", GastoViewSet)

urlpatterns = router.urls
