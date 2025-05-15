from connexionDB import db

class Budget:
    _collection = db['budgets']

    def __init__(self, departement, budget_alloue, budget_consomme):
        self.departement = departement
        self.budget_alloue = budget_alloue
        self.budget_consomme = budget_consomme
        self.budget_disponible = budget_alloue - budget_consomme

    def save(self):
        data = {
            'departement': self.departement,
            'budget_alloue': self.budget_alloue,
            'budget_consomme': self.budget_consomme,
            'budget_disponible': self.budget_disponible
        }
        return self._collection.insert_one(data)

    @classmethod
    def tous(cls):
        return list(cls._collection.find({}))

    @classmethod
    def trouver_par_departement(cls, departement):
        return cls._collection.find_one({'departement': departement})

    @classmethod
    def ajouter_ou_mettre_a_jour(cls, departement, budget_alloue, budget_consomme=0):
        budget_existant = cls.trouver_par_departement(departement)
        
        if budget_existant:
            # Mise à jour du budget existant
            nouveau_alloue = budget_existant['budget_alloue'] + budget_alloue
            nouveau_consomme = budget_existant['budget_consomme'] + budget_consomme
            nouveau_disponible = nouveau_alloue - nouveau_consomme
            
            cls._collection.update_one(
                {'_id': budget_existant['_id']},
                {
                    '$set': {
                        'budget_alloue': nouveau_alloue,
                        'budget_consomme': nouveau_consomme,
                        'budget_disponible': nouveau_disponible
                    }
                }
            )
            return cls._collection.find_one({'_id': budget_existant['_id']})
        else:
            # Création d'un nouveau budget
            nouveau_budget = cls(departement, budget_alloue, budget_consomme)
            result = nouveau_budget.save()
            return cls._collection.find_one({'_id': result.inserted_id})

    @classmethod
    def mettre_a_jour_budget_consomme(cls, departement, nouveau_consomme):
        budget = cls.trouver_par_departement(departement)
        if budget:
            nouveau_disponible = budget['budget_alloue'] - nouveau_consomme
            cls._collection.update_one(
                {'_id': budget['_id']},
                {
                    '$set': {
                        'budget_consomme': nouveau_consomme,
                        'budget_disponible': nouveau_disponible
                    }
                }
            )
            return True
        return False
    