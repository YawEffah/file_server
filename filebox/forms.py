from .models import UploadedFile
from django import forms


class FileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['title', 'description', 'file']   
    
  