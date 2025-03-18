from .whoscored_data_extractor import WhoScoredDataExtractor
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
import json

@api_view(['POST'])
@parser_classes([JSONParser])
def extract_whoscored_data(request):
    try:
        # Extraire les paramètres du corps de la requête
        player_name = request.data.get("player_name")
        html_path = request.data.get("html_path")

        # Vérifier que les paramètres sont présents
        if not player_name or not html_path:
            return Response({"error": "Missing required parameters: 'player_name' and 'html_path'."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Effectuer l'extraction des données
        extractor = WhoScoredDataExtractor(html_path)
        data = extractor.extract_player_stats_and_events(player_name)
        
        # Retourner la réponse
        response = Response(json.loads(data), status=status.HTTP_200_OK)
        response['Content-Disposition'] = f'attachment; filename="{player_name.replace(" ", "_")}_data.json"'
        return response
    
    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON body."}, status=status.HTTP_400_BAD_REQUEST)
