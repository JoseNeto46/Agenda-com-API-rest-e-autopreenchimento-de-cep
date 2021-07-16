from rest_framework import routers, serializers, viewsets
from .models import Contato


class ContatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contato
        fields = ['nome']
