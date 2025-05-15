from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Devis
from demandeAchat.models import DemandeAchat
from bson import json_util
import json
from bson import ObjectId
import json
import base64

@csrf_exempt
@csrf_exempt
def ajouter_devis(request):
    if request.method == 'POST':
        try:
            if not request.content_type.startswith('multipart/form-data'):
                return JsonResponse({
                    "status": "error",
                    "message": "Content-Type doit être multipart/form-data"
                }, status=400)

            # Récupération des données du formulaire
            data = request.POST.dict()
            photo_file = request.FILES.get('photo_signature')

            # Lecture des données binaires de l'image
            photo_data = photo_file.read() if photo_file else None

            # Validation des références matériel
            references_materiel = [ref.strip() for ref in data.get('reference_materiel', '').split(',')]
            
            # Vérification des demandes existantes
            toutes_demandes = DemandeAchat.tous()
            for ref in references_materiel:
                if not any(d.get('reference') == ref for d in toutes_demandes):
                    return JsonResponse({
                        "status": "error",
                        "message": f"Demande introuvable: {ref}"
                    }, status=404)

            # Récupération du statut du devis
            status_devis = data.get('status_devis', 'en_attente')

            # Création du nouveau devis
            montant_total = float(request.POST.get("montant_total", 0)) 
            nouvel_devis = Devis(
                reference_devis=data.get('reference_devis'),
                nom_departement=data.get('nom_departement'),
                nom_fournisseur=data.get('nom_fournisseur'),
                reference_materiel=data.get('reference_materiel'),
                date_devis=data.get('date_devis'),
                nom_materiel=data.get('nom_materiel'),
                quantite=data.get('quantite') or data.get('qte_materiel'),
                prix_unitaire=data.get('prix_unitaire'),
                montant_total=montant_total,
                status_devis=status_devis,
                photo_signature=photo_data,
            )

            # Sauvegarde du devis
            devis_id = nouvel_devis.save()

            # Mise à jour du statut des demandes selon le statut du devis
            new_status = 'en_cours' if status_devis != 'rejeté' else 'rejeté'
            
            for ref in references_materiel:
                DemandeAchat._collection.update_one(
                    {'reference': ref},
                    {'$set': {'status': new_status}}
                )

            return JsonResponse({
                'status': 'success',
                'id': str(devis_id),
                'message': 'Devis créé avec succès'
            })

        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=500)

    return JsonResponse({
        "status": "error",
        "message": "Méthode non autorisée"
    }, status=405)

def liste_devis(request):
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
    
def demandes_par_departement(request, departement):
    try:
        toutes_demandes = DemandeAchat.tous()
        references = []
        
        for dmd in toutes_demandes:
            # Vérifier que le département correspond (insensible à la casse)
            # ET que le statut est "en attente"
            if ('departement' in dmd 
                and dmd['departement'].lower() == departement.lower()
                and dmd.get('status') == "en_attente"):
                references.append(dmd['reference'])
        
        return JsonResponse({
            'status': 'success',
            'departement': departement,
            'references': references,
            'count': len(references)
        }, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
    
def details_demande(request, reference):
    try:
        # Récupérer toutes les demandes
        toutes_demandes = DemandeAchat.tous()
        
        # Filtrer pour trouver la demande avec la référence exacte
        demande_trouvee = next(
            (d for d in toutes_demandes if d.get('reference') == reference),
            None
        )
        
        if demande_trouvee:
            response_data = {
                'reference': demande_trouvee.get('reference'),
                'natureDemande': demande_trouvee.get('natureDemande'),
                'quantite': demande_trouvee.get('quantite'),
                'departement': demande_trouvee.get('departement'),
                'status': demande_trouvee.get('status')
            }
            return JsonResponse({
                'status': 'success',
                'data': response_data
            }, status=200)
        else:
            return JsonResponse({
                'status': 'error',
                'message': f'Aucune demande trouvée avec la référence: {reference}'
            }, status=404)
            
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)
    