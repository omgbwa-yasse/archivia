from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db import transaction
import json

from .models import User, Group, UserGroup, Role, Permission, AccessControl

def login_view(request):
    if request.user.is_authenticated:
        return redirect('users:welcome')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not all([email, password]):
            messages.error(request, 'Veuillez remplir tous les champs')
            return redirect('users:login')
            
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('users:welcome')
        else:
            messages.error(request, 'Email ou mot de passe incorrect')
            return redirect('users:login')
            
    return render(request, 'users/login.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('users:welcome')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        if not all([username, email, password, password_confirm]):
            messages.error(request, 'Veuillez remplir tous les champs obligatoires')
            return redirect('users:register')
            
        if password != password_confirm:
            messages.error(request, 'Les mots de passe ne correspondent pas')
            return redirect('users:register')
            
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            login(request, user)
            messages.success(request, 'Compte créé avec succès')
            return redirect('users:welcome')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('users:register')
            
    return render(request, 'users/register.html')

@login_required
def welcome(request):
    return render(request, 'users/welcome.html')

@login_required
def profile(request):
    if request.method == 'POST':
        # Handle profile update
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.save()
        messages.success(request, 'Profil mis à jour avec succès')
        return redirect('users:profile')
    
    return render(request, 'users/profile.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès')
    return redirect('users:login')

@login_required
@require_http_methods(["GET", "PUT", "DELETE"])
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == "GET":
        return JsonResponse({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'enabled': user.enabled
        })
    
    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            
            if 'first_name' in data:
                user.first_name = data['first_name']
            if 'last_name' in data:
                user.last_name = data['last_name']
            if 'enabled' in data:
                user.enabled = data['enabled']
                
            user.save()
            return JsonResponse({'message': 'User updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    elif request.method == "DELETE":
        user.enabled = False
        user.save()
        return JsonResponse({'message': 'User disabled successfully'})

@login_required
@require_http_methods(["GET", "POST"])
def group_views(request):
    if request.method == "GET":
        groups = Group.objects.filter(deleted_at__isnull=True)
        return JsonResponse({
            'groups': [{
                'id': group.id,
                'name': group.name,
                'description': group.description,
                'parent_id': group.parent_id
            } for group in groups]
        })
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            group = Group.objects.create(
                name=data['name'],
                description=data.get('description'),
                parent_id=data.get('parent_id'),
                created_by=request.user
            )
            return JsonResponse({
                'id': group.id,
                'name': group.name,
                'description': group.description,
                'parent_id': group.parent_id
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@login_required
@require_http_methods(["GET", "PUT", "DELETE"])
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id, deleted_at__isnull=True)
    
    if request.method == "GET":
        return JsonResponse({
            'id': group.id,
            'name': group.name,
            'description': group.description,
            'parent_id': group.parent_id
        })
    
    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            
            if 'name' in data:
                group.name = data['name']
            if 'description' in data:
                group.description = data['description']
            if 'parent_id' in data:
                group.parent_id = data['parent_id']
                
            group.updated_by = request.user
            group.save()
            return JsonResponse({'message': 'Group updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    elif request.method == "DELETE":
        group.deleted_by = request.user
        group.save()
        return JsonResponse({'message': 'Group deleted successfully'})

@login_required
@require_http_methods(["POST"])
def add_user_to_group(request, group_id):
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        role = data.get('role', 'MEMBER')

        user = get_object_or_404(User, id=user_id)
        group = get_object_or_404(Group, id=group_id)

        user_group = UserGroup.objects.create(
            user=user,
            group=group,
            role=role,
            created_by=request.user
        )

        return JsonResponse({'message': 'User added to group successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def settings(request):
    if request.method == 'POST':
        # Handle settings update
        user = request.user
        user.email = request.POST.get('email', user.email)
        user.save()
        messages.success(request, 'Paramètres mis à jour avec succès')
        return redirect('users:settings')
    
    return render(request, 'users/settings.html') 