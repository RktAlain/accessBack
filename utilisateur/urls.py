from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('ajouter/', views.ajouter_utilisateur, name='ajouter_utilisateur'),
    path('afficher_tous/', views.liste_utilisateurs, name='liste_utilisateurs'),
    path('activer/<str:id_utilisateur>/', views.activer_utilisateur, name='activer_utilisateur'),
    path('desactiver/<str:id_utilisateur>/', views.desactiver_utilisateur, name='desactiver_utilisateur'),
    path('supprimer/<str:id_utilisateur>/', views.supprimer_utilisateur, name='supprimer_utilisateur'),
    path('afficher/<str:id_utilisateur>/', views.liste_utilisateur_par_id, name='liste_utilisateur_par_id'),
    path('afficher_par_email/<str:email>/', views.liste_utilisateur_par_email, name='liste_utilisateur_par_email'),
    
]