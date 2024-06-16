from django.dispatch import Signal
from django.dispatch import receiver
from .models import UploadedFile


file_downloaded = Signal()
file_shared = Signal()

@receiver(file_downloaded, sender=UploadedFile)
def update_download_count(sender, instance, **kwargs):
    instance.download_count += 1
    instance.save()


@receiver(file_shared, sender=UploadedFile)
def update_share_count(sender, instance, **kwargs):
    instance.share_count += 1
    instance.save()




