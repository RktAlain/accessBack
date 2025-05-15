from connexionDB import db
from bson.binary import Binary
from bson.objectid import ObjectId

class Devis:
    _collection = db['devis']

    def __init__(self, reference_devis, nom_departement, nom_fournisseur,
                 reference_materiel, date_devis, nom_materiel, quantite,
                 prix_unitaire, montant_total, status_devis, photo_signature=None):
        self.reference_devis = reference_devis
        self.nom_departement = nom_departement
        self.nom_fournisseur = nom_fournisseur
        self.reference_materiel = reference_materiel
        self.date_devis = date_devis
        self.nom_materiel = nom_materiel
        self.quantite = quantite
        self.prix_unitaire = prix_unitaire
        self.montant_total = montant_total
        self.status_devis = status_devis
        self.photo_signature = photo_signature

    def save(self):
        # Conversion de l'image en format binaire pour MongoDB
        photo_binaire = Binary(self.photo_signature) if self.photo_signature else None

        data = {
            'reference_devis': self.reference_devis,
            'nom_departement': self.nom_departement,
            'nom_fournisseur': self.nom_fournisseur,
            'reference_materiel': self.reference_materiel,
            'date_devis': self.date_devis,
            'nom_materiel': self.nom_materiel,
            'quantite': self.quantite,
            'prix_unitaire': self.prix_unitaire,
            'montant_total': self.montant_total,
            'status_devis': self.status_devis,
            'photo_signature': photo_binaire,
        }
        return self._collection.insert_one(data).inserted_id

    @classmethod
    def tous(cls):
        return list(cls._collection.find({}))
    
    @classmethod
    def maj_photo_et_statut(cls, devis_id, nouvelle_photo):
        # Vérifie que l'ID est valide
        if not ObjectId.is_valid(devis_id):
            return None
        
        # Convertit l'image en format binaire pour MongoDB
        photo_binaire = Binary(nouvelle_photo) if nouvelle_photo else None
        
        # Met à jour la photo de signature ET le statut
        result = cls._collection.update_one(
            {'_id': ObjectId(devis_id)},
            {'$set': {
                'photo_signature': photo_binaire,
                'status_devis': 'approuvé'  # Mise à jour du statut
            }}
        )
        
        return result.modified_count > 0