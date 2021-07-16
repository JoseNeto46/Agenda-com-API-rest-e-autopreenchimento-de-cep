from django.urls import path
from . import views

urlpatterns = [
    path('', views.contatos_list_view, name='contatos_list_view'),
    path('grupos/<int:grupo_id>/contatos/', views.contatos_list_view, name='contatos_list_por_grupo'),
    path('editar/<int:contato_id>/', views.editar_contato, name='editar_contato'),
    path('novo-grupo/', views.novo_grupo_view, name='novo_grupo'),
    path('novo-contato/', views.novo_contato_view, name='novo_contato'),
    path('<int:contato_id>/novo_tel', views.novo_tel_view, name='novo_tel'),
    path('<int:contato_id>/novo_email/', views.novo_email_view, name='novo_email'),
    path('<int:contato_id>/novo_endereco/', views.novo_endereco_view, name='novo_endereco'),
    path('<int:contato_id>/excluir/', views.excluir_contato_view, name='excluir_contato'),
    path('<int:contato_id>/telefone/<label>/excluir/', views.excluir_telefone_view, name='excluir_telefone'),
    path('<int:contato_id>/email/<label>/excluir/', views.excluir_email_view, name='excluir_email'),
    path('grupos/', views.grupos_list_view, name='grupos_list'),
    path('grupos/<int:grupo_id>/editar/', views.editar_grupo, name='editar_grupo'),
    path('grupos/<int:grupo_id>/excluir/', views.excluir_grupo, name='excluir_grupo'),
]
