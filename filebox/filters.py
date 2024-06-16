import django_filters
from django.forms import TextInput
from .models import UploadedFile
from django_filters import CharFilter



class FileFilter(django_filters.FilterSet):
    title = CharFilter(field_name="title", lookup_expr='icontains', widget=TextInput(attrs={'placeholder': 'Search by title...'}))
    class Meta:
        model = UploadedFile
        fields = ['title']
      
