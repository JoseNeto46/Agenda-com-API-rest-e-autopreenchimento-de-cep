from django.contrib import admin
from .models import Contato, Grupo, Email, Telefone, Endereco


@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']


@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']


@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ['rua', 'bairro', 'num', 'contato']


@admin.register(Telefone)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ['numero', 'contato']


@admin.register(Email)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ['endereco_email', 'contato']
