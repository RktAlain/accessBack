from django.urls import path
from . import views

urlpatterns = [
    path('ajouterDevis/', views.ajouter_devis, name='ajouter_devis'),
    path('listeDevis/', views.liste_devis, name='liste_devis'),
    path('listeDemandes/', views.liste_demandes, name='liste_demandes'),
    path('demandesParDepartement/<str:departement>/', views.demandes_par_departement, name='demandes_par_departement'),
    path('detailsDemande/<str:reference>/', views.details_demande, name='details_demande'),
]