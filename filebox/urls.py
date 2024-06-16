from django.urls import path
from . import views
from accounts import views as accountsviews


app_name = 'filebox'
urlpatterns = [
    path('login/', accountsviews.login_view, name='login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
   
    path('upload/', views.upload_view, name='upload'),
    path('update/<int:file_id>', views.update_view, name='update'),
    path('delete/<int:file_id>', views.delelte_view, name='delete'),
    
]