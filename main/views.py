from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404

from main.forms import PersonForm, UserSignUpForm
from main.models import Person
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required


# Create your views here.
def users(request):
    users = Person.objects.all().order_by('-created_at')
    return render(request, 'users.html', {'users': users})

@login_required
def add_user(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,
                             "A new user has been created successfully!")
            return redirect('users')
    else:
        form = PersonForm()
    return render(request, 'add_user.html', {'form': form})

@login_required
def delete_user(request, pk):
    users = get_object_or_404(Person, pk=pk)
    if request.method == 'POST':
        users.delete()
        return redirect('users')
    return render(request, 'delete_user.html', {'users': users})

@login_required
def edit_user(request, pk):
    users = get_object_or_404(Person, pk=pk)
    if request.method == 'POST':
        form = PersonForm(request.POST, instance=users)
        if form.is_valid():
            form.save()
            messages.success(request,
                             f"Call for {users.first_name} has been successfully updated!")
            return redirect('users')
    else:
        form = PersonForm(instance=users)
    return render(request, 'edit_user.html', {'form': form, 'users': users})



def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('users')  
    else:
        form = UserSignUpForm()

    return render(request, 'signup.html', {'form': form})

def userlogin(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You are now logged in!')
            return redirect('users')  # Redirect after login
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def userlogout(request):
        logout(request)
        return redirect('users')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Prevents logout after password change
            messages.success(request, 'Your password was successfully updated!')
            return redirect('users')  # Redirect to the users list or dashboard
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'change_password.html', {'form': form})