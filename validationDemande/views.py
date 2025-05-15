from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from achatDevis.models import Devis
from demandeAchat.models import DemandeAchat
from bson import json_util
import json
from bson import ObjectId
import json
import base64

def liste_validations(request):
    try:
        devis = Devis.tous()
        devis_liste = []
        
        for d in devis:
            # Conversion de l'image binaire en base64
            photo_base64 = None
            if d.get('photo_signature'):
                photo_base64 = base64.b64encode(d['photo_signature']).decode('utf-8')

            devis_data = {
                'id': str(d['_id']),
                'reference_devis': d.get('reference_devis'),
                'nom_departement': d.get('nom_departement'),
                'nom_fournisseur': d.get('nom_fournisseur'),
                'reference_materiel': d.get('reference_materiel'),
                'date_devis': d.get('date_devis'),
                'nom_materiel': d.get('nom_materiel'),
                'quantite': d.get('quantite') or d.get('qte_materiel'),
                'prix_unitaire': d.get('prix_unitaire'),
                'montant_total': d.get('montant_total'),
                'status_devis': d.get('status_devis'),
                'photo_signature': photo_base64
            }
            devis_liste.append(devis_data)

        return JsonResponse({
            'status': 'success',
            'data': devis_liste
        }, safe=False)

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
    
@csrf_exempt
def maj_photo_devis(request, devis_id):
    if request.method == 'POST':
        try:
            # Vérification du content-type
            if not request.content_type.startswith('multipart/form-data'):
                return JsonResponse({
                    "status": "error",
                    "message": "Content-Type doit être multipart/form-data"
                }, status=400)

            # Récupération du fichier image
            photo_file = request.FILES.get('photo_signature')
            if not photo_file:
                return JsonResponse({
                    "status": "error",
                    "message": "Aucune photo fournie"
                }, status=400)

            # Lecture des données binaires de l'image
            photo_data = photo_file.read()

            # Mise à jour de la photo et du statut dans la base de données
            success = Devis.maj_photo_et_statut(devis_id, photo_data)
            
            if success:
                return JsonResponse({
                    "status": "success",
                    "message": "Photo mise à jour et devis approuvé avec succès"
                })
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "Devis non trouvé ou aucune modification effectuée"
                }, status=404)

        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=500)

    return JsonResponse({
        "status": "error",
        "message": "Méthode non autorisée"
    }, status=405)

@csrf_exempt
def approver_demande(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            reference_materiel = data.get('reference_materiel', '')
            
            if not reference_materiel:
                return JsonResponse({
                    "status": "error",
                    "message": "Le paramètre reference_materiel est requis"
                }, status=400)
            
            # Séparer les références
            references = [ref.strip() for ref in reference_materiel.split(',')]
            results = []
            
            for ref in references:
                # Vérifier si la demande existe
                demande = DemandeAchat._collection.find_one({'reference': ref})
                
                if not demande:
                    results.append({
                        "reference": ref,
                        "status": "error",
                        "message": "Demande introuvable"
                    })
                    continue
                
                # Mettre à jour le statut
                result = DemandeAchat._collection.update_one(
                    {'reference': ref},
                    {'$set': {'status': 'Approuvé'}}
                )
                
                if result.modified_count == 1:
                    results.append({
                        "reference": ref,
                        "status": "success",
                        "message": "Statut mis à jour avec succès"
                    })
                else:
                    results.append({
                        "reference": ref,
                        "status": "error",
                        "message": "Échec de la mise à jour"
                    })
            
            return JsonResponse({
                "status": "completed",
                "results": results
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                "status": "error",
                "message": "Données JSON invalides"
            }, status=400)
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=500)
    
    return JsonResponse({
        "status": "error",
        "message": "Méthode non autorisée"
    }, status=405)