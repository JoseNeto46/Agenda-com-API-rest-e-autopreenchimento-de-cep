from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from contatos.views import ContatoViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'contatos', ContatoViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('', include('contatos.urls')),
    path('api-auth/', include('rest_framework.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # caminho para acessar urls das imagens
