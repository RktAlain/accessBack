from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from achatDevis.models import Devis
import json
from .models import Budget

@csrf_exempt
def ajouter_budget(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            departement = data.get('departement')
            budget_alloue = float(data.get('budget_alloue', 0))
            budget_consomme = float(data.get('budget_consomme', 0))
            
            Budget.ajouter_ou_mettre_a_jour(departement, budget_alloue, budget_consomme)
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

def liste_budgets(request):
    try:
        budgets = Budget.tous()
        budgets_liste = []
        for budget in budgets:
            budget_data = {
                'id': str(budget['_id']),
                'departement': budget['departement'],
                'budget_alloue': budget['budget_alloue'],
                'budget_consomme': budget['budget_consomme'],
                'budget_disponible': budget['budget_disponible'],
            }
            budgets_liste.append(budget_data)
        return JsonResponse({'status': 'success', 'data': budgets_liste}, status=200)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

def montants_approuves_par_departement(request):
    try:
        # Récupérer tous les devis approuvés groupés par département
        devis_approuves = Devis._collection.aggregate([
            {
                '$match': {
                    'status_devis': 'approuvé'
                }
            },
            {
                '$group': {
                    '_id': '$nom_departement',
                    'total_montant': {'$sum': '$montant_total'},
                    'nombre_devis': {'$sum': 1}
                }
            },
            {
                '$project': {
                    'departement': '$_id',
                    'total_montant': 1,
                    'nombre_devis': 1,
                    '_id': 0
                }
            },
            {
                '$sort': {'departement': 1}
            }
        ])

        # Convertir le curseur en liste
        resultats = list(devis_approuves)

        # Mettre à jour les budgets consommés pour chaque département
        for resultat in resultats:
            Budget.mettre_a_jour_budget_consomme(
                resultat['departement'],
                resultat['total_montant']
            )

        return JsonResponse({
            'status': 'success',
            'data': resultats,
            'message': 'Budgets mis à jour avec succès'
        }, status=200)

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
    
def budgets_disponibles_par_departement(request):
    try:
        # Récupérer tous les budgets groupés par département
        budgets = Budget._collection.aggregate([
            {
                '$group': {
                    '_id': '$departement',
                    'budget_alloue': {'$sum': '$budget_alloue'},
                    'budget_consomme': {'$sum': '$budget_consomme'},
                    'budget_disponible': {'$sum': '$budget_disponible'}
                }
            },
            {
                '$project': {
                    'departement': '$_id',
                    'budget_alloue': 1,
                    'budget_consomme': 1,
                    'budget_disponible': 1,
                    '_id': 0
                }
            },
            {
                '$sort': {'departement': 1}
            }
        ])

        # Convertir le curseur en liste
        resultats = list(budgets)

        return JsonResponse({
            'status': 'success',
            'data': resultats
        }, status=200)

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)