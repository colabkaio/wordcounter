from django.urls import path
# Importa as views que
# vão ser usadas nas rotas
from . import views


urlpatterns = [
    # Definindo a rota base, no caso, '/'
    path('', views.index, name='index'),
    path('results', views.results, name='results')
]