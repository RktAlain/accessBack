from connexionDB import db
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId
import traceback
from django.http import JsonResponse

class Article:
    _collection = db['articles']  # Collection MongoDB pour les articles

    def __init__(self, nom, reference, categorie, quantite, seuil_alerte=1, emplacement='', statut='actif'):
        self.nom = nom
        self.reference = reference
        self.categorie = categorie
        self.quantite = quantite
        self.seuil_alerte = seuil_alerte
        self.emplacement = emplacement
        self.statut = statut
        self.date_creation = datetime.utcnow()

    def save(self):
        """Sauvegarde un article dans la base de données MongoDB."""
        data = {
            'nom': self.nom,
            'reference': self.reference,
            'categorie': self.categorie,
            'quantite': self.quantite,
            'seuil_alerte': self.seuil_alerte,
            'emplacement': self.emplacement,
            'statut': self.statut,
            'date_creation': self.date_creation
        }
        return self._collection.insert_one(data).inserted_id

    @classmethod
    def tous(cls):
        """Récupère tous les articles présents dans la collection."""
        return list(cls._collection.find({}))

    @classmethod
    def trouver_par_id(cls, article_id):
        """Récupère un article par son ID MongoDB."""
        try:
            return cls._collection.find_one({'_id': ObjectId(article_id)})
        except (InvalidId, TypeError):
            return None

    @classmethod
    def trouver_par_reference(cls, reference):
        """Récupère un article par sa référence unique."""
        return cls._collection.find_one({'reference': reference})

    @classmethod
    def mettre_a_jour_par_id(cls, article_id, **kwargs):
        """Met à jour un article dans la base de données par son ID."""
        try:
            return cls._collection.update_one(
                {'_id': ObjectId(article_id)},
                {'$set': kwargs}
            )
        except (InvalidId, TypeError):
            return None

    @classmethod
    def ajouter_mouvement(cls, reference, quantite, type_mouvement):
        """Ajoute un mouvement d'article (entrée/sortie) et met à jour la quantité de stock."""
        article = cls.trouver_par_reference(reference)

        if not article:
            return {'status': 'error', 'message': 'Article non trouvé'}

        nouvelle_quantite = article['quantite']

        # Gestion des types de mouvements
        if type_mouvement == 'entree':
            nouvelle_quantite += quantite
        elif type_mouvement == 'sortie':
            if article['quantite'] < quantite:
                return {'status': 'error', 'message': 'Stock insuffisant'}
            nouvelle_quantite -= quantite
        else:
            return {'status': 'error', 'message': 'Type de mouvement invalide'}

        # Mise à jour de l'article avec la nouvelle quantité
        cls.mettre_a_jour_par_reference(reference, quantite=nouvelle_quantite)

        return {'status': 'success', 'message': 'Mouvement enregistré'}

    @classmethod
    def mettre_a_jour_par_reference(cls, reference, **kwargs):
        """Met à jour un article par sa référence unique."""
        try:
            return cls._collection.update_one(
                {'reference': reference},
                {'$set': kwargs}
            )
        except (InvalidId, TypeError):
            return None

    def __str__(self):
        """Représentation textuelle de l'article."""
        return f"{self.nom} ({self.reference}) - {self.emplacement} - {self.statut}"

