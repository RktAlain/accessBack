from connexionDB import db
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId
import traceback
from django.http import JsonResponse

class MouvementStock:
    _collection = db['mouvements_stock']  # Collection MongoDB pour les mouvements de stock

    def __init__(self, nom_article, reference, quantite, type_mouvement, date_mouvement=None):
        """
        :param nom_article: Le nom de l'article (comme clé étrangère logique)
        :param reference: Référence de l'article
        :param quantite: Quantité de mouvement
        :param type_mouvement: Type de mouvement ('entree' ou 'sortie')
        :param date_mouvement: Date du mouvement
        """
        self.nom_article = nom_article
        self.reference = reference
        self.quantite = quantite
        self.type_mouvement = type_mouvement
        self.date_mouvement = date_mouvement or datetime.utcnow()  # Date par défaut à maintenant

    def save(self):
        """Sauvegarde un mouvement de stock dans la collection MongoDB"""
        data = {
            'nom_article': self.nom_article,  # Nom de l'article en tant que clé étrangère logique
            'reference': self.reference,
            'quantite': self.quantite,
            'type_mouvement': self.type_mouvement,
            'date_mouvement': self.date_mouvement
        }
        try:
            return self._collection.insert_one(data).inserted_id
        except Exception as e:
            return {'status': 'error', 'message': f'Erreur lors de la sauvegarde : {str(e)}'}

    @classmethod
    def tous(cls):
        """Récupère tous les mouvements de stock"""
        try:
            return list(cls._collection.find({}))
        except Exception as e:
            return {'status': 'error', 'message': f'Erreur lors de la récupération des mouvements : {str(e)}'}
    @classmethod
    def trouver_par_type(cls, mouvement_type):
        """Récupère tous les mouvements d'un type spécifique (entree/retrait)"""
        try:
            return list(cls._collection.find({'type_mouvement': mouvement_type}))
        except Exception as e:
            return {'status': 'error', 'message': f'Erreur lors de la récupération des mouvements de type {mouvement_type}: {str(e)}'}
        
    @classmethod
    def trouver_par_reference(cls, reference):
        """Récupère tous les mouvements d'un article par sa référence"""
        try:
            return list(cls._collection.find({'reference': reference}))
        except Exception as e:
            return {'status': 'error', 'message': f'Erreur lors de la récupération des mouvements pour la référence {reference}: {str(e)}'}

    @classmethod
    def trouver_par_nom_article(cls, nom_article):
        """Récupère tous les mouvements d'un article par son nom"""
        try:
            return list(cls._collection.find({'nom_article': nom_article}))
        except Exception as e:
            return {'status': 'error', 'message': f'Erreur lors de la récupération des mouvements pour l\'article {nom_article}: {str(e)}'}

    @classmethod
    def trouver_par_id(cls, mouvement_id):
        """Récupère un mouvement de stock par son ID MongoDB"""
        try:
            return cls._collection.find_one({'_id': ObjectId(mouvement_id)})
        except (InvalidId, TypeError):
            return None
        except Exception as e:
            return {'status': 'error', 'message': f'Erreur lors de la récupération du mouvement : {str(e)}'}

    @classmethod
    def mettre_a_jour_par_id(cls, mouvement_id, **kwargs):
        """Met à jour un mouvement de stock par son ID"""
        try:
            return cls._collection.update_one(
                {'_id': ObjectId(mouvement_id)},
                {'$set': kwargs}
            )
        except (InvalidId, TypeError):
            return None
        except Exception as e:
            return {'status': 'error', 'message': f'Erreur lors de la mise à jour du mouvement : {str(e)}'}

    def __str__(self):
        """Représentation textuelle du mouvement de stock"""
        return f"{self.nom_article} ({self.reference}) - {self.type_mouvement} - {self.quantite} unités"
