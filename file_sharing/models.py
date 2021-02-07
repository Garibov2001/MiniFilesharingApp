from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch import receiver

PERMISSION_CHOICES = (
    (0, "Read Only"),
    (1, "Read and Comment"),
)


class FilePost(models.Model):
    document = models.FileField(upload_to='uploaded_files')
    description = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_shared_info(self):
        return self.filesharing_set.all()

    def __str__(self):
        return self.description


class FileSharing(models.Model):
    document = models.ForeignKey(FilePost, on_delete=models.CASCADE)
    shared_user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission =  models.IntegerField(choices=PERMISSION_CHOICES, default= 1) 

    def __str__(self):
        return self.description



class FileComment(models.Model):
    document = models.ForeignKey(FilePost, on_delete=models.CASCADE)
    comment_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    comment_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.description


class UserLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    operating_system = models.CharField(max_length=50)
    browser = models.CharField(max_length=50)
    ip_address = models.CharField(max_length=50)
    log_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.description




