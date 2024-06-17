from django.db import models
from django.utils import timezone
from accounts.models import User



# Model for uploaded files
class UploadedFile(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=150)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, related_name='uploaded_files', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"


# Model to track downloads
class Download(models.Model):
    user = models.ForeignKey(User, related_name='downloads', on_delete=models.CASCADE)
    file = models.ForeignKey(UploadedFile, related_name='downloads', on_delete=models.CASCADE)
    downloaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} downloaded {self.file.title}'


# Model to track emails sent
class Email(models.Model):
    user = models.ForeignKey(User, related_name='sent_emails', on_delete=models.CASCADE)
    file = models.ForeignKey(UploadedFile, related_name='sent_emails', on_delete=models.CASCADE)
    recipient_email = models.EmailField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} sent {self.file.title} to {self.recipient_email}'





