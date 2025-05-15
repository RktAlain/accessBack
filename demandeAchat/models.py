from connexionDB import db
from datetime import datetime
from bson import ObjectId

class DemandeAchat:
    _collection = db['demandes_achat']  # Collection MongoDB

    def __init__(self, demandeur_id, natureDemande, departement, description,
                 quantite=1, urgence='moyenne', impactStrategique='moyen',
                 justification='', siConfidentiel=False,
                 status='en_attente', reference=None):
        self.demandeur_id = demandeur_id
        self.natureDemande = natureDemande
        self.departement = departement
        self.description = description
        self.quantite = quantite
        self.urgence = urgence
        self.impactStrategique = impactStrategique
        self.justification = justification
        self.siConfidentiel = siConfidentiel
        self.status = status
        self.reference = reference
        self.dateDemande = datetime.now()

    def save(self):
        """Sauvegarde la demande dans MongoDB"""
        data = {
            'demandeur_id': self.demandeur_id,
            'natureDemande': self.natureDemande,
            'departement': self.departement,
            'description': self.description,
            'quantite': self.quantite,
            'urgence': self.urgence,
            'impactStrategique': self.impactStrategique,
            'justification': self.justification,
            'siConfidentiel': self.siConfidentiel,
            'status': self.status,
            'dateDemande': self.dateDemande
        }

        # Gestion de la référence automatique
        if not self.reference:
            # Compter le nombre de documents pour générer la référence
            count = self._collection.count_documents({})
            self.reference = f"DA-{str(count + 1).zfill(5)}"
            data['reference'] = self.reference

        result = self._collection.insert_one(data)
        return result.inserted_id
    
    @classmethod
    def objects(cls):
        """Simule le Manager de Django"""
        return cls

    @classmethod
    def trouver_par_reference(cls, reference):
        """Récupère une demande par sa référence"""
        return cls._collection.find_one({'reference': reference})

    @classmethod
    def tous(cls):
        """Récupère toutes les demandes"""
        return list(cls._collection.find({}))

    @classmethod
    def filter(cls, **kwargs):
        """Filtre les demandes"""
        return list(cls._collection.find(kwargs))

    @classmethod
    def trouver_par_demandeur(cls, demandeur_id):
        """Récupère les demandes d'un demandeur spécifique"""
        return list(cls._collection.find({'demandeur_id': demandeur_id}))

    @classmethod
    def mettre_a_jour(cls, reference, **kwargs):
        """Met à jour une demande"""
        update_data = {k: v for k, v in kwargs.items() if v is not None}
        if update_data:
            return cls._collection.update_one(
                {'reference': reference},
                {'$set': update_data}
            )
        return None

    @classmethod
    def supprimer(cls, reference):
        """Supprime une demande"""
        return cls._collection.delete_one({'reference': reference})

    @classmethod
    def approuver(cls, reference):
        """Approuve une demande"""
        return cls._collection.update_one(
            {'reference': reference},
            {'$set': {'status': 'approuvee'}}
        )

    @classmethod
    def rejeter(cls, reference):
        """Rejette une demande"""
        return cls._collection.update_one(
            {'reference': reference},
            {'$set': {'status': 'rejetee'}}
        )