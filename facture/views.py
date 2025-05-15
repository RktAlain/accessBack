from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Facture
import json

@csrf_exempt
def ajouter_factures(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nouvelle_facture = Facture(
                Num_Facture=data.get('Num_Facture'),
                Date_facture=data.get('Date_facture'),
                Fournisseur=data.get('Fournisseur'),
                Matériel=data.get('Matériel'),
                Département=data.get('Département'),
                Montant=data.get('Montant'),
            )
            facture_id = nouvelle_facture.save()
            return JsonResponse({'id': str(facture_id), 'status': 'success'})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

def liste_factures(request):
    try:
        factures = Facture.tous()
        factures_liste = []
        for facture in factures:
            facture_data = {
                'id': str(facture['_id']),
                'Num_Facture': facture['Num_Facture'],
                'Date_facture': facture['Date_facture'],
                'Fournisseur': facture['Fournisseur'],
                'Matériel': facture['Matériel'],
                'Département': facture['Département'],
                'Montant': facture['Montant'],
            }
            factures_liste.append(facture_data)
        return JsonResponse({'status': 'success', 'data': factures_liste}, status=200)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
