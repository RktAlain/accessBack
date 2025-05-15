from django.urls import path
from . import views

urlpatterns = [
    path('listeValidations/', views.liste_validations, name='liste_validations'),
    path('majPhotoDevis/<str:devis_id>/', views.maj_photo_devis, name='maj_photo_devis'),
    path('approverDemande/', views.approver_demande, name='approver_demande'),
]