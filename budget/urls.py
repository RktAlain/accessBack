from django.urls import path
from . import views

urlpatterns = [
    path('ajouterBudgets/', views.ajouter_budget, name='ajouter_budgets'),
    path('listeBudgets/', views.liste_budgets, name='liste_budgets'),
    path('montantsApprouvesParDepartement/', views.montants_approuves_par_departement, name='montants_approuves_par_departement'),
    path('budgetsDisponiblesParDepartement/', views.budgets_disponibles_par_departement, name='budgets_disponibles_par_departement'),
    
]