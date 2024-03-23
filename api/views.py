import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

headers = {
            "X-RapidAPI-Key": "5176d5cbeemsh987a57f90719806p112791jsnd75cd19fea41",
            "X-RapidAPI-Host": "imdb188.p.rapidapi.com"
        }

class WeekTop(APIView):
    def get(self, request):
        url = "https://imdb188.p.rapidapi.com/api/v1/getWeekTop10"


        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raises an HTTPError if the response code is 4XX/5XX
            data = response.json()["data"]  # Assuming 'data' contains the list of top movies/shows

            # Extracting required fields
            extracted_data = []
            for item in data:
                extracted_item = {
                    "id": item.get("id", {}),
                    "title": item.get("titleText", {}).get("text", "N/A"),
                    "rating":item.get("ratingsSummary",{}).get("aggregateRating",0),
                    "description": item.get("plot", {}).get("plotText", {}).get("plainText", "N/A"),
                    "release_date": f"{item.get('releaseDate', {}).get('year', 'N/A')}-{item.get('releaseDate', {}).get('month', 'N/A'):02d}-{item.get('releaseDate', {}).get('day', 'N/A'):02d}",
                    "image": item.get("primaryImage", {}).get("imageUrl", "N/A")
                }
                extracted_data.append(extracted_item)

            return Response(extracted_data, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        
class MovieLookup(APIView):
    def get(self, request):
        url = "https://api.frembed.fun/movies?order=popular"
        try:
            res = requests.get(url)
            res.raise_for_status()
            data = res.json()['result']
            
            extracted_data = []
            for item in data['items']:
                extracted_item = {
                    "id": item.get("imdb", {}),
                    "title": item.get("title", {}),
                    "description": item.get("plot", {}).get("plotText", {}).get("plainText", "N/A"),
                    "release_date": item.get('year', {}),
                    "link": item.get("link", {})
                }
                extracted_data.append(extracted_item)

            return Response(extracted_data, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            
            
