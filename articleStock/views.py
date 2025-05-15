from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Article
import json
import traceback
from bson.errors import InvalidId

def json_response(status, message, data=None, status_code=200):
    response = {'status': status, 'message': message}
    if data is not None:
        response['data'] = data
    return JsonResponse(response, status=status_code)

@csrf_exempt
def article_view(request, article_id=None):
    try:
        if request.method == 'GET':
            if article_id:
                try:
                    article = Article.trouver_par_id(article_id)
                    if not article:
                        return json_response('error', 'Article non trouvé', status_code=404)
                    
                    return json_response('success', 'Article trouvé', {
                        'id': str(article['_id']),
                        'nom': article['nom'],
                        'reference': article['reference'],
                        'categorie': article['categorie'],
                        'quantite': article['quantite'],
                        'seuil_alerte': article['seuil_alerte'],
                        'emplacement': article['emplacement'],
                        'date_creation': article.get('date_creation', None)
                    })
                except InvalidId:
                    return json_response('error', 'ID invalide', status_code=400)
                except Exception as e:
                    return json_response('error', str(e), status_code=500)
            else:
                try:
                    articles = Article.tous()
                    return json_response('success', 'Articles récupérés', [
                        {
                            'id': str(a['_id']),
                            'nom': a['nom'],
                            'reference': a['reference'],
                            'categorie': a['categorie'],
                            'quantite': a['quantite'],
                            'seuil_alerte': a['seuil_alerte'],
                            'emplacement': a['emplacement'],
                            'date_creation': a.get('date_creation', None)
                        } for a in articles
                    ])
                except Exception as e:
                    return json_response('error', str(e), status_code=500)
        
        elif request.method == 'POST':
            try:
                data = json.loads(request.body)
                required_fields = ['nom', 'reference', 'categorie', 'quantite', 'emplacement']
                if any(field not in data for field in required_fields):
                    return json_response('error', 'Champs obligatoires manquants', status_code=400)
                if Article.trouver_par_reference(data['reference']):
                    return json_response('error', 'Référence déjà utilisée', status_code=400)
                
                article = Article(**data)
                article_id = article.save()
                return json_response('success', 'Article créé', {'id': str(article_id), 'nom': article.nom}, status_code=201)
            except json.JSONDecodeError:
                return json_response('error', 'JSON invalide', status_code=400)
            except ValueError:
                return json_response('error', 'Quantité doit être un nombre', status_code=400)
            except Exception as e:
                traceback.print_exc()
                return json_response('error', str(e), status_code=500)
        
        elif request.method == 'DELETE':
            if not article_id:
                return json_response('error', 'ID requis', status_code=400)
            try:
                result = Article.supprimer_par_id(article_id)
                if not result or result.deleted_count == 0:
                    return json_response('error', 'Article non trouvé', status_code=404)
                return json_response('success', 'Article supprimé')
            except InvalidId:
                return json_response('error', 'ID invalide', status_code=400)
            except Exception as e:
                return json_response('error', str(e), status_code=500)
        
        return json_response('error', 'Méthode non autorisée', status_code=405)
    except Exception as e:
        traceback.print_exc()
        return json_response('error', str(e), status_code=500)

