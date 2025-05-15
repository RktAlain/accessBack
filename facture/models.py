from connexionDB import db
from bson import ObjectId


class Facture:
    _collection = db['factures'] 

    def __init__(self, Num_Facture, Date_facture, Fournisseur, Matériel, Département, Montant):
        self.Num_Facture = Num_Facture
        self.Date_facture = Date_facture
        self.Fournisseur = Fournisseur
        self.Matériel = Matériel
        self.Département = Département
        self.Montant = Montant

    def save(self):
        data = {
            'Num_Facture': self.Num_Facture,
            'Date_facture': self.Date_facture,
            'Fournisseur': self.Fournisseur,
            'Matériel': self.Matériel,
            'Département': self.Département,
            'Montant': self.Montant
        }
        return self._collection.insert_one(data).inserted_id
    
    @classmethod
    def tous(cls):
        return list(cls._collection.find({}))