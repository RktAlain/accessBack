# stockMouvement/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models_stock_mouvement import MouvementStock
from articleStock.models import Article
import json
import traceback
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId

def json_response(status, message, data=None, status_code=200):
    response = {'status': status, 'message': message}
    if data is not None:
        response['data'] = data
    return JsonResponse(response, status=status_code)

@csrf_exempt
def article_movement(request, article_id=None):
    try:
        if request.method == 'GET':
            if article_id:
                article = Article.trouver_par_id(article_id)
                if not article:
                    return json_response('error', 'Article non trouvé', status_code=404)
                mouvements = MouvementStock.tous_filtre({'reference': article['reference']})
            else:
                mouvements = MouvementStock.tous()  # Récupérer tous les mouvements si aucun article_id

            mouvements_list = [
                {
                    'id': str(m['_id']),
                    'nom_article': m.get('nom_article', ''),
                    'quantite': m.get('quantite', 0),
                    'type_mouvement': m.get('type_mouvement', ''),
                    'date_mouvement': m.get('date_mouvement', datetime.utcnow()).isoformat(),
                    'reference': m.get('reference', '')
                } for m in mouvements
            ]

            return json_response('success', 'Mouvements récupérés', mouvements_list)


        elif request.method == 'POST':
            try:
                data = json.loads(request.body)
                action = data.get('action')
                quantite = int(data.get('quantite', 0))

                if action not in ['entrer', 'retrait']:
                    return json_response('error', 'Action invalide', status_code=400)

                if quantite <= 0:
                    return json_response('error', 'Quantité invalide', status_code=400)

                article = Article.trouver_par_id(article_id)
                if not article:
                    return json_response('error', 'Article non trouvé', status_code=404)

                if action == 'retrait' and article['quantite'] < quantite:
                    return json_response('error', 'Stock insuffisant', status_code=400)

                new_quantity = article['quantite'] + quantite if action == 'entrer' else article['quantite'] - quantite

                update_result = Article.mettre_a_jour_par_id(
                    article_id, 
                    quantite=new_quantity,
                    date_modification=datetime.utcnow()
                )

                if not update_result:
                    return json_response('error', 'Échec mise à jour', status_code=500)

                stock_mouvement = MouvementStock(
                    nom_article=article['nom'],
                    reference=article['reference'],
                    quantite=quantite,
                    type_mouvement=action
                )
                mouvement_id = stock_mouvement.save()

                return json_response('success', 'Mouvement enregistré', {
                    'id': str(mouvement_id),
                    'nouvelle_quantite': new_quantity
                })

            except json.JSONDecodeError:
                return json_response('error', 'JSON invalide', status_code=400)
            except ValueError:
                return json_response('error', 'Quantité doit être un nombre', status_code=400)
            except Exception as e:
                traceback.print_exc()
                return json_response('error', str(e), status_code=500)

        return json_response('error', 'Méthode non supportée', status_code=405)

    except Exception as e:
        traceback.print_exc()
        return json_response('error', str(e), status_code=500)