from connexionDB import db
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from datetime import datetime


class Utilisateur:
    _collection = db['utilisateurs'] 

    def __init__(self, nom, email, mdp, role, departement=None, statut='actif', date_ajout=None, date_derniere_connexion=None):
        self.nom = nom
        self.email = email
        self.mdp = generate_password_hash(mdp)
        self.role = role
        self.departement = departement  # Nouvel attribut
        self.statut = statut  # Nouvel attribut avec valeur par défaut
        self.date_ajout = date_ajout if date_ajout else datetime.now()  # Nouvel attribut
        self.date_derniere_connexion = date_derniere_connexion  # Nouvel attribut

    def save(self):
        data = {
            'nom': self.nom,
            'email': self.email,
            'mdp': self.mdp,
            'role': self.role,
            'departement': self.departement,  # Nouvel attribut
            'statut': self.statut,  # Nouvel attribut
            'date_ajout': self.date_ajout,  # Nouvel attribut
            'date_derniere_connexion': self.date_derniere_connexion  # Nouvel attribut
        }
        return self._collection.insert_one(data).inserted_id

    @classmethod
    def trouver_par_email(cls, email):
        return cls._collection.find_one({'email': email})

    @classmethod
    def trouver_par_id(cls, user_id):
        return cls._collection.find_one({'_id': ObjectId(user_id)})
    
    @classmethod
    def tous(cls):
        return list(cls._collection.find({}))

    @classmethod
    def mettre_a_jour(cls, user_id, **kwargs):
        if 'mdp' in kwargs:
            kwargs['mdp'] = generate_password_hash(kwargs['mdp'])
        if 'date_derniere_connexion' in kwargs and kwargs['date_derniere_connexion'] is None:
            kwargs['date_derniere_connexion'] = datetime.now()
        return cls._collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': kwargs}
        )
        
    @classmethod
    def supprimer(cls, user_id):
        return cls._collection.delete_one({'_id': ObjectId(user_id)})