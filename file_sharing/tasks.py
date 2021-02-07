from celery import shared_task
from celery.decorators import periodic_task
from file_sharing.models import FilePost

from datetime import datetime, timedelta

# at 00:00 o clock to check life cycle
@periodic_task(run_every=(crontab(day='0 0 * * *')), name="clean_operation", ignore_result=True)
def remove_files():
    for file in FilePost.objects.all():
        result = datetime.today() - file.date_posted
        if result.days > 7:
            file.delete()

