from django.urls import path
from . import views
from accounts import views as accountsviews


app_name = 'filebox'
urlpatterns = [
    path('login/', accountsviews.login_view, name='login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('upload/', views.upload_view, name='upload'),
    path('update/<int:file_id>', views.update_view, name='update'),
    path('delete/<int:file_id>', views.delete_view, name='delete'),
    path('download/<int:file_id>', views.download_file, name='download_file'),
    path('share/<int:file_id>', views.share_file, name='share_file')
]