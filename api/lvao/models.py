from django.db import models
from .utils import call_api_address_gouv
import csv
import hashlib


# Create your models here.

class CSVFileProcess(models.Model):

    file = models.FileField(upload_to='csv_files/')
    status_choices = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='pending')
    progress = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    total = models.IntegerField(default=0)
    error_message = models.TextField(blank=True, null=True)
    # Add any other fields you might need to track related to the CSV processing

    
    def clean_column_name(self, name):
        # Remove invisible characters, whitespace, and BOM from column names
        return ''.join(filter(lambda x: x.isprintable() and not x.isspace() and ord(x) != 65279, name))


    def clean_data(self):
        try:
            self.status = 'processing'
            self.total = self.count_csv_rows()
            self.save()
            self.import_rows()
        except Exception as e:
            self.status = 'failed'
            self.error_message = str(e)
            self.save()
        self.progress = 100
        self.status = 'completed'
        self.save()

    def count_csv_rows(self):
        try:
            with open(self.file.path, newline='') as csvfile:
                reader = csv.reader(csvfile)
                total_rows = sum(1 for row in reader)
                return total_rows
        except FileNotFoundError:
            print("File not found.")
            return 0  # Or handle the error as needed

    def import_rows(self):
        with open(self.file.path, newline='', encoding='utf-8-sig') as csvfile:  # Use utf-8-sig to handle BOM
            reader = csv.DictReader(csvfile)
            current_row = 0
            for row in reader:
                cleaned_row = {self.clean_column_name(key): value for key, value in row.items()}
                current_row = current_row + 1
                self.progress = 100 * current_row / self.total
                print(self.progress)
                self.save()

                (csvdata,_) = CSVData.objects.update_or_create(
                    slug=cleaned_row['identifiant_unique'],
                    defaults={
                        'adress1':cleaned_row['adresse'],
                        'adress2':cleaned_row['adresse_complement'],
                        'zipcode':cleaned_row['code_postal'],
                        'city':cleaned_row['ville'],
                        'lat':float(cleaned_row['st_x']) if cleaned_row['st_x'] != '' else None,
                        'long':float(cleaned_row['st_y']) if cleaned_row['st_y'] != '' else None,
                    }
                )

                # if has not been cleaned yet
                if(csvdata.generate_md5_address() != csvdata.cleaned_address_for_hash):
                    csvdata.clean_data()

    def __str__(self):
        return f"CSV Process - ID: {self.id}, Status: {self.status}"

class CSVData(models.Model):
    slug = models.CharField(max_length=100)
    adress1 = models.CharField(max_length=2048, null=True)
    adress2 = models.CharField(max_length=2048, blank=True, null=True)
    zipcode = models.CharField(max_length=20, null=True)
    city = models.CharField(max_length=100, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    long = models.DecimalField(max_digits=9, decimal_places=6, null=True)

    data_gouv_json = models.JSONField(default=None, null=True)
    data_gouv_score = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    error = models.CharField(max_length=2048, null=True, default=None)

    cleaned_address_for_hash = models.CharField(max_length=2048, null=True, default=None)
    cleaned_gps_for_hash = models.CharField(max_length=2048, null=True, default=None)

    cleaned_address = models.CharField(max_length=2048, null=True)
    cleaned_zipcode = models.CharField(max_length=20, null=True)
    cleaned_city = models.CharField(max_length=100, null=True)
    cleaned_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    cleaned_long = models.DecimalField(max_digits=9, decimal_places=6, null=True)

    def clean_data(self):
        try:
            response = call_api_address_gouv(self.adress1, self.adress2,self.zipcode,self.city)
            self.data_gouv_json = response
            properties = response.get('features')[0].get('properties')
            geometry = response.get('features')[0].get('geometry')

            self.data_gouv_score = properties.get('score')

            self.cleaned_address_for_hash = self.generate_md5_address()
            self.cleaned_address = properties.get('name')
            self.cleaned_zipcode = properties.get('postcode')
            self.cleaned_city = properties.get('city')
            self.cleaned_lat = geometry.get('coordinates')[0]
            self.cleaned_long = geometry.get('coordinates')[1]

            self.save()
        except Exception as e:
            self.error = str(e)
            self.save()


    def generate_md5_address(self):
        # Concatenate the values
        concatenated_string = f"{self.adress1}{self.adress2}{self.zipcode}{self.city}"

        # Create an MD5 hash object
        md5_hash = hashlib.md5()

        # Update the hash object with the concatenated string (encoded as UTF-8)
        md5_hash.update(concatenated_string.encode('utf-8'))

        # Get the hexadecimal representation of the MD5 hash
        md5_value = md5_hash.hexdigest()

        return md5_value
    
    def __str__(self):
        return self.slug 