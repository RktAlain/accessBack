from rest_framework import serializers
from .models import Article  # Importer ton modèle Article

class ArticleSerializer(serializers.Serializer):
    nom = serializers.CharField(max_length=255)
    reference = serializers.CharField(max_length=255)
    categorie = serializers.CharField(max_length=255)
    quantite = serializers.IntegerField()
    seuil_alerte = serializers.IntegerField(default=1)
    emplacement = serializers.CharField(max_length=255, required=False)
    statut = serializers.CharField(max_length=255, default='actif')
    date_creation = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        # Créer un article à partir des données validées
        return Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Mettre à jour un article existant
        instance.nom = validated_data.get('nom', instance.nom)
        instance.reference = validated_data.get('reference', instance.reference)
        instance.categorie = validated_data.get('categorie', instance.categorie)
        instance.quantite = validated_data.get('quantite', instance.quantite)
        instance.seuil_alerte = validated_data.get('seuil_alerte', instance.seuil_alerte)
        instance.emplacement = validated_data.get('emplacement', instance.emplacement)
        instance.statut = validated_data.get('statut', instance.statut)
        instance.save()
        return instance
