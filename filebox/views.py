from django.shortcuts import render, redirect
from .forms import FileForm
from .models import UploadedFile, Download, Email
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from .filters import FileFilter
from django.http import FileResponse
from django.core.mail import EmailMessage
import mimetypes
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Count


# Utility function to check if the user is an admin
def is_admin(user):
    return user.groups.filter(name='admin').exists()


# Redirects the user to the appropriate dashboard based on roles.
@login_required
def index(request):
    if is_admin(request.user):
        return redirect('filebox:admin_dashboard')
    else:
        return redirect('filebox:user_dashboard')
    

# Admin dashboard view for managing files and viewing analytics
def admin_dashboard(request):
    files = UploadedFile.objects.all().annotate(
        download_count=Count('downloads'),
        share_count=Count('sent_emails')
    ).order_by('-id')
    myFilter = FileFilter(request.GET, queryset=files)
    filtered_files = myFilter.qs

    context = {
        'file_upload_form': FileForm(),
        'files': filtered_files,
        'myFilter': myFilter,
        'recent_files': UploadedFile.objects.order_by('-uploaded_at')[:3],
    }

    return render(request, 'filebox/admin-dashboard.html', context)


# Dashboard for customer to view and download files
@login_required
def user_dashboard(request):
    if is_admin(request.user):  # Redirect admin to admin dashboard
        return redirect('filebox:admin_dashboard')
    
    files = UploadedFile.objects.all().order_by('-id')
    myFilter = FileFilter(request.GET, queryset=files)
    filtered_files = myFilter.qs

    context = {
        'files': filtered_files,
        'myFilter': myFilter,
        'recent_files': UploadedFile.objects.order_by('-uploaded_at')[:3],
    }

    return render(request, 'filebox/user-dashboard.html', context)


# Function to handle file uploads
@login_required
@user_passes_test(is_admin, login_url='login')
def upload_view(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.uploaded_at = timezone.now()
            form.instance.uploaded_by = request.user
            form.save()
            messages.success(request, "File successfully uploaded")
            return redirect(reverse('filebox:admin_dashboard'))
        else:
            messages.error(request, "File upload failed! Please try again.")
            return redirect(reverse('filebox:admin_dashboard'))
        

# Function to update files
@login_required
@user_passes_test(is_admin, login_url='login')
def update_view(request, file_id):
    file = UploadedFile.objects.get(pk=file_id)
    form = FileForm(request.POST or None, instance=file)
    if form.is_valid():
        form.save()
        messages.success(request, 'File successfully updated')
        return redirect('filebox:admin_dashboard')
    return render(request, 'filebox/update.html', {'edit_form': form})


# This function delete objects
@login_required
@user_passes_test(is_admin, login_url='login')
def delete_view(request, file_id):
    file = UploadedFile.objects.get(pk=file_id)
    file.delete()
    messages.success(request, 'File successfully deleted')
    return redirect('filebox:admin_dashboard')


# File download view (Handles file downloads)
@login_required
def download_file(request, file_id):
    downloaded_file = UploadedFile.objects.get(id=file_id)
    response = FileResponse(downloaded_file.file.open('rb'))
    file_mime_type, _ = mimetypes.guess_type(downloaded_file.file.name)
    
    response['Content-Type'] = file_mime_type or 'application/octet-stream'
    response['Content-Disposition'] = f'attachment; filename="{downloaded_file.file.name}"'
   
    # Create a Download record
    Download.objects.create(
        user=request.user,
        file=downloaded_file,
        downloaded_at=timezone.now()
    )

    return response


# File sharing view (Handles how files are shared via email)
@login_required
def share_file(request, file_id):
    try:
        shared_file = UploadedFile.objects.get(id=file_id)
    except UploadedFile.DoesNotExist:
        messages.error(request, "File not found.")
        return redirect(reverse('filebox:user_dashboard'))
    
    if request.method == "POST":
        recipient_email = request.POST.get('email')
        if recipient_email:
            try:
                validate_email(recipient_email)
                email = EmailMessage(
                    subject=f"Shared File: {shared_file.title}",
                    body=f"Hello,\n\nA file titled '{shared_file.title}' has been shared with you by {request.user.first_name}.\n\nDescription: {shared_file.description}\n\nBest regards,\nFilebox Team",
                    from_email='filebox.notifications@gmail.com',
                    to=[recipient_email],
                )
                email.attach_file(shared_file.file.path)
                email.send(fail_silently=False)

                # Create an Email record
                Email.objects.create(
                    user=request.user,
                    file=shared_file,
                    recipient_email=recipient_email,
                )
                
                messages.success(request, "File successfully shared.")
            except ValidationError:
                messages.error(request, "Invalid email address provided.")
            except Exception as e:
                messages.error(request, "There was an error sending the email. Please try again.")
        else:
            messages.error(request, "No email address provided.")
        return redirect(reverse('filebox:user_dashboard'))

    return redirect(reverse('filebox:user_dashboard'))
