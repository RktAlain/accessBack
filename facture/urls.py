from django.urls import path
from . import views

urlpatterns = [
    path('ajouterFactures/', views.ajouter_factures, name='ajouter_factures'),
    path('listeFactures/', views.liste_factures, name='liste_factures'),
    
]