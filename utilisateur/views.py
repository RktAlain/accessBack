from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Utilisateur
from bson import json_util
import json
from bson import ObjectId
from werkzeug.security import check_password_hash
import jwt
from datetime import datetime, timedelta
from django.conf import settings

@csrf_exempt
def ajouter_utilisateur(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nouvel_utilisateur = Utilisateur(
                nom=data.get('nom'),
                email=data.get('email'),
                mdp=data.get('mdp'),
                role=data.get('role'),
                departement=data.get('departement', ''),  # Nouvel attribut
                statut=data.get('statut', 'actif'),  # Nouvel attribut avec valeur par défaut
                date_ajout=datetime.now(),  # Nouvel attribut
                date_derniere_connexion=None  # Nouvel attribut initialisé à None
            )
            user_id = nouvel_utilisateur.save()
            return JsonResponse({'id': str(user_id), 'status': 'success'})
        except Exception as e:
            return JsonResponse({"status":"error","message ":str(e)}, status=500)

def liste_utilisateurs(request):
    try:
        utilisateurs = Utilisateur.tous()
        utilisateurs_liste = []
        for utilisateur in utilisateurs:
            utilisateur_data = {
                'id': str(utilisateur['_id']),
                'nom': utilisateur['nom'],
                'email': utilisateur['email'],
                'role': utilisateur['role'],
                'departement': utilisateur.get('departement', ''),  # Nouvel attribut
                'statut': utilisateur.get('statut', 'actif'),  # Nouvel attribut
                'date_ajout': utilisateur.get('date_ajout', ''),  # Nouvel attribut
                'date_derniere_connexion': utilisateur.get('date_derniere_connexion', ''),  # Nouvel attribut
                # Note: On ne devrait pas renvoyer le mot de passe dans la réponse
                'mdp': utilisateur['mdp'],
            }
            utilisateurs_liste.append(utilisateur_data)
        return JsonResponse({'status': 'success', 'data': utilisateurs_liste}, status=200)
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@csrf_exempt
def liste_utilisateur_par_id(request, id_utilisateur):
    try:
        if not ObjectId.is_valid(id_utilisateur):
            return JsonResponse({'error': 'ID utilisateur invalide'}, status=400)

        utilisateur = Utilisateur.trouver_par_id(id_utilisateur)
        if not utilisateur:
            return JsonResponse(
            {'error': 'Utilisateur non trouvé par cet ID'},
            status=404
        )
        
        data = json.loads(json_util.dumps(utilisateur))
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse(
            {'error': f'Erreur de recuperation: {str(e)}'},
            status=500
        )
        
        
@csrf_exempt
def liste_utilisateur_par_email(request, email):
    try:
        utilisateur = Utilisateur.trouver_par_email(email)
        
        if not utilisateur:
            return JsonResponse(
            {'error': 'Utilisateur non trouvé par cet email'},
            status=404
        )
        
        data = json.loads(json_util.dumps(utilisateur))
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse(
            {'error': f'Erreur de recuperation: {str(e)}'},
            status=500
        )
    
@csrf_exempt
def desactiver_utilisateur(request, id_utilisateur):
    if request.method == 'PUT':  # ou 'POST' selon vos préférences
        try:
            if not ObjectId.is_valid(id_utilisateur):
                return JsonResponse({'error': 'ID utilisateur invalide'}, status=400)

            # Mettre à jour seulement le statut
            result = Utilisateur.mettre_a_jour(
                user_id=id_utilisateur,
                statut='inactif'
            )
            
            if result.modified_count == 0:
                return JsonResponse({'error': 'Utilisateur non trouvé ou déjà inactif'}, status=404)
                
            return JsonResponse({
                'success': True, 
                'message': 'Utilisateur désactivé avec succès',
                'statut': 'inactif'
            }, status=200)
            
        except Exception as e:
            return JsonResponse(
                {'error': f'Erreur de désactivation: {str(e)}'},
                status=500
            )
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@csrf_exempt
def activer_utilisateur(request, id_utilisateur):
    if request.method == 'PUT':  # ou 'POST' selon vos préférences
        try:
            if not ObjectId.is_valid(id_utilisateur):
                return JsonResponse({'error': 'ID utilisateur invalide'}, status=400)

            # Mettre à jour seulement le statut
            result = Utilisateur.mettre_a_jour(
                user_id=id_utilisateur,
                statut='actif'
            )
            
            if result.modified_count == 0:
                return JsonResponse({'error': 'Utilisateur non trouvé ou déjà actif'}, status=404)
                
            return JsonResponse({
                'success': True, 
                'message': 'Utilisateur activé avec succès',
                'statut': 'actif'
            }, status=200)
            
        except Exception as e:
            return JsonResponse(
                {'error': f'Erreur d\'activation: {str(e)}'},
                status=500
            )
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@csrf_exempt
def supprimer_utilisateur(request, id_utilisateur):
    try:
        if not ObjectId.is_valid(id_utilisateur):
            return JsonResponse({'error': 'ID utilisateur invalide'}, status=400)

        result = Utilisateur.supprimer(id_utilisateur)
        
        if result.deleted_count == 0:
            return JsonResponse({'error': 'Utilisateur non trouvé'}, status=404)
            
        return JsonResponse({'success': True, 'message': 'Utilisateur supprimé'})
        
    except Exception as e:
        return JsonResponse(
            {'error': f'Erreur de suppression: {str(e)}'},
            status=500
        )

def mettre_a_jour(self, **kwargs):
    if 'email' in kwargs and kwargs['email'] != self.email:
        if Utilisateur.trouver_par_email(kwargs['email']):
            raise ValueError("Cet email est déjà utilisé")
    
    update_data = {}
    for champ, valeur in kwargs.items():
        if hasattr(self, champ):
            setattr(self, champ, valeur)
            update_data[champ] = valeur
    
    if update_data:
        from bson import ObjectId
        return Utilisateur.mettre_a_jour(
            {'_id': ObjectId(self._id)},
            {'$set': update_data}
        ).modified_count > 0
    return False

def generate_jwt(user_data):
    payload = {
        'id': str(user_data['id']),
        'email': user_data['email'],
        'exp': datetime.utcnow() + timedelta(days=1),  # Expiration dans 1 jour
        'iat': datetime.utcnow(),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

@csrf_exempt 
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            mdp = data.get('mdp')
            role = data.get('role').lower()
            
            user_data = json.loads(json_util.dumps(Utilisateur.trouver_par_email(email)))
            
            print(user_data)
            if user_data and check_password_hash(user_data['mdp'], mdp) and user_data['role'].lower() == role:
                # Mettre à jour la date de dernière connexion
                Utilisateur.mettre_a_jour(
                    {'_id': ObjectId(user_data['_id']['$oid'])},
                    {'$set': {'date_derniere_connexion': datetime.now()}}
                )
                
                user_info = {
                    'id': str(user_data['_id']['$oid']),
                    'nom': user_data['nom'],
                    'email': user_data['email'],
                    'role': user_data['role'],
                    'departement': user_data.get('departement', ''),
                    'statut': user_data.get('statut', 'actif'),
                    'message': 'Connexion réussie'
                }
                
                token = generate_jwt(user_info)
                return JsonResponse({"user_info": user_info, "token": token}, status=200)
            else:
                return JsonResponse({'error': 'Email ou rôle ou mot de passe incorrect'}, status=401)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)