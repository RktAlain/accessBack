from django.http import JsonResponse, HttpResponse
from .models import DemandeAchat
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def creer_demande(request):
    if request.method == 'POST':
        try:
            # Pour les données JSON
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST
            
            nouvelle_demande = DemandeAchat(
                demandeur_id=data.get('demandeur_id'),
                natureDemande=data.get('natureDemande'),
                departement=data.get('departement'),
                description=data.get('description'),
                quantite=data.get('quantite', 1),
                urgence=data.get('urgence', 'moyenne'),
                impactStrategique=data.get('impactStrategique', 'moyen'),
                justification=data.get('justification'),
                siConfidentiel=data.get('siConfidentiel', False)
            )
            
            # Gestion du fichier si envoyé
            if 'pieceJustificative' in request.FILES:
                nouvelle_demande.pieceJustificative = request.FILES['pieceJustificative']
            
            demande_id = nouvelle_demande.save()
            return JsonResponse({
                'id': str(demande_id),
                'reference': nouvelle_demande.reference,
                'status': 'success'
            }, status=201)
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

def liste_demandes(request):
    try:
        demandes = DemandeAchat.tous()
        demandes_list = []
  
        for dmd in demandes:
            dmd_data = {
                'id': str(dmd['_id']),
                'demandeur_id': dmd['demandeur_id'],
                'natureDemande': dmd['natureDemande'],
                'departement': dmd['departement'],
                'description': dmd['description'],
                'urgence': dmd['urgence'],
                'impactStrategique': dmd['impactStrategique'],
                'justification': dmd['justification'],
                'siConfidentiel': dmd['siConfidentiel'],
                'quantite': dmd['quantite'],
                'status': dmd['status'],
                'reference': dmd['reference'],
                'dateDemande': dmd['dateDemande'].isoformat() if 'dateDemande' in dmd else None
            }
            demandes_list.append(dmd_data)

        return JsonResponse({'status': 'success', 'data': demandes_list}, status=200)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

def details_demande(request, reference):
    try:
        demande = DemandeAchat.trouver_par_reference(reference)
        if not demande:
            return JsonResponse({
                'status': 'error',
                'message': 'Demande non trouvée'
            }, status=404)
            
        demande_data = {
            'reference': demande.get('reference'),
            'dateDemande': demande.get('dateDemande').isoformat() if demande.get('dateDemande') else None,
            'demandeur_id': demande.get('demandeur_id'),
            'status': demande.get('status'),
            'natureDemande': demande.get('natureDemande'),
            'departement': demande.get('departement'),
            'description': demande.get('description'),
            'quantite': demande.get('quantite'),
            'urgence': demande.get('urgence'),
            'impactStrategique': demande.get('impactStrategique'),
            'justification': demande.get('justification'),
            'siConfidentiel': demande.get('siConfidentiel'),
            'pieceJustificative': demande.get('pieceJustificative')
        }
        return JsonResponse({
            'status': 'success',
            'demande': demande_data
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@csrf_exempt
def mettre_a_jour_demande(request, reference):
    if request.method == 'POST':
        try:
            demande = DemandeAchat.trouver_par_reference(reference)
            if not demande:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Demande non trouvée'
                }, status=404)
            
            # Pour les données JSON
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST
            
            # Mise à jour des champs
            update_data = {}
            fields_to_update = [
                'natureDemande', 'departement', 'description',
                'quantite', 'urgence', 'impactStrategique',
                'justification', 'siConfidentiel', 'status'
            ]
            
            for field in fields_to_update:
                if field in data:
                    update_data[field] = data[field]
            
            # Gestion du fichier
            if 'pieceJustificative' in request.FILES:
                update_data['pieceJustificative'] = request.FILES['pieceJustificative']
            
            # Effectuer la mise à jour
            DemandeAchat.mettre_a_jour(reference, **update_data)
            
            return JsonResponse({
                'status': 'success',
                'message': 'Demande mise à jour',
                'reference': reference
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

@csrf_exempt
def supprimer_demande(request, reference):
    if request.method == 'POST':
        try:
            result = DemandeAchat.supprimer(reference)
            if result.deleted_count == 0:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Demande non trouvée'
                }, status=404)
                
            return JsonResponse({
                'status': 'success',
                'message': 'Demande supprimée'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

@csrf_exempt
def approuver_demande(request, reference):
    if request.method == 'POST':
        try:
            result = DemandeAchat.approuver(reference)
            if result.modified_count == 0:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Demande non trouvée ou déjà approuvée'
                }, status=404)
                
            return JsonResponse({
                'status': 'success',
                'message': 'Demande approuvée',
                'reference': reference
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

@csrf_exempt
def rejeter_demande(request, reference):
    if request.method == 'POST':
        try:
            result = DemandeAchat.rejeter(reference)
            if result.modified_count == 0:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Demande non trouvée ou déjà rejetée'
                }, status=404)
                
            return JsonResponse({
                'status': 'success',
                'message': 'Demande rejetée',
                'reference': reference
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)