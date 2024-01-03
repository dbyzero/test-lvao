from django.contrib import admin
from .models import CSVFileProcess, CSVData

@admin.register(CSVFileProcess)
class CSVFileProcessAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'status', 'progress', 'total')
    search_fields = ('file',)
    list_filter = ('status',)
    readonly_fields = ('id', 'error_message', 'total')  # Fields that should be read-only in the admin


@admin.register(CSVData)
class CSVDataAdmin(admin.ModelAdmin):
    list_display = ('slug', 'adress1', 'adress2', 'zipcode', 'city', 'lat', 'long')
