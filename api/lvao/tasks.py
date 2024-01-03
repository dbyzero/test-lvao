from celery import shared_task

@shared_task
def run_clean_csv():
    from .models import CSVFileProcess

    csv_file_to_process = CSVFileProcess.objects.filter(
        status='pending'
    ).all()

    print(csv_file_to_process)

    for csv_file in csv_file_to_process:
        print(f"Start clean file {csv_file.id}")
        csv_file.clean_data()

    return True