import csv

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from django.http import HttpResponse
from .models import CSVData, CSVFileProcess

from .utils import calculate_distance

# Create your views here.

class CSVFileProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = CSVFileProcess
        fields = ('id', 'file', 'status', 'progress', 'error_message', 'total')

        
class CSVFileProcessViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CSVFileProcess.objects.all()
    serializer_class = CSVFileProcessSerializer
    
    def get_queryset(self):
        queryset = CSVFileProcess.objects.exclude(status__in=['completed', 'failed']).order_by('id')
        return queryset

class CSVFileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        serializer = CSVFileProcessSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(status='pending')  # Save with pending status
            # Implement your processing logic here (e.g., using a task queue like Celery)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def download_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['identifiant_unique', 'adresse', 'adresse_complement', 'code_postal', 'ville', 'st_x', 'st_y', 'addresse corrigé', 'distance en mètre des nouvelles coordonnées'])

    csv_data = CSVData.objects.all()
    for row in csv_data:
        if row.data_gouv_score is not None:
            delta = calculate_distance(row.lat, row.long, row.cleaned_lat, row.cleaned_long)
            writer.writerow([row.slug, row.cleaned_address, None, row.cleaned_zipcode, row.cleaned_city, row.cleaned_lat, row.cleaned_long, 'oui', int(delta * 1000) if delta is not None else None])
        else:
            writer.writerow([row.slug, row.adress1, row.adress2, row.zipcode, row.city, row.lat, row.long, 'non', None])

    return response