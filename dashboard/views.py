from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from core.models import Service, Category
from django.contrib.auth.models import User

# Decorator to ensure only admin can access
def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def service_list(request):
    services = Service.objects.all().select_related('category')
    return render(request, 'dashboard/service_list.html', {'services': services})

@login_required
@user_passes_test(is_admin)
def settings_view(request):
    if request.method == 'POST':
        # Handle "User ID" (Username) change
        if 'update_profile' in request.POST:
            new_username = request.POST.get('username')
            if new_username:
                if User.objects.filter(username=new_username).exclude(pk=request.user.pk).exists():
                     messages.error(request, "Username already exists.")
                else:
                    request.user.username = new_username
                    request.user.save()
                    messages.success(request, "Profile updated successfully.")
            return redirect('dashboard:settings')
        
        # Handle Password change
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, "Your password was successfully updated!")
                return redirect('dashboard:settings')
            else:
                messages.error(request, "Please correct the error below.")
    else:
        password_form = PasswordChangeForm(request.user)

    return render(request, 'dashboard/settings.html', {
        'password_form': password_form,
        'user': request.user
    })
