from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from feature_requests import views

router = routers.DefaultRouter()
router.register(r'clients', views.ClientsViewSet)
router.register(r'projects', views.ProjectsViewSet)
router.register(r'features', views.FeaturesViewSet)
router.register(r'product-area', views.ProductAreaViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^maxvalue/', views.return_max_value),
]