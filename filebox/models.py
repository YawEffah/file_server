from django.db import models
from django.utils import timezone


class UploadedFile(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=150)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    download_count = models.IntegerField(default=0)
    share_count = models.IntegerField(default=0)


    def __str__(self):
        return f" {self.title}"


