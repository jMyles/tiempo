from rest_framework import routers

from tiempo.contrib.django_app.views import TiempoHistoryViewSet

tiempo_api_router = routers.DefaultRouter()
tiempo_api_router.register(r'jobs', TiempoHistoryViewSet, "Job")