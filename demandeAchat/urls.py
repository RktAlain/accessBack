from django.urls import path
from .views import (
    creer_demande,
    liste_demandes,
    details_demande,
    mettre_a_jour_demande,
    supprimer_demande,
    approuver_demande,
    rejeter_demande
)

urlpatterns = [
    path('creer/', creer_demande, name='creer_demande'),
    path('demandes/', liste_demandes, name='liste_demandes'),
    path('demandes/<str:reference>/', details_demande, name='details_demande'),
    path('demandes/<str:reference>/mettre-a-jour/', mettre_a_jour_demande, name='mettre_a_jour_demande'),
    path('demandes/<str:reference>/supprimer/', supprimer_demande, name='supprimer_demande'),
    path('demandes/<str:reference>/approuver/', approuver_demande, name='approuver_demande'),
    path('demandes/<str:reference>/rejeter/', rejeter_demande, name='rejeter_demande'),
]