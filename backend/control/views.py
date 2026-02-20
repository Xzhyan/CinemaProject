from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

# Forms
from .forms import UserLoginForm, AddSessionForm, AddFilmCardForm, AddCategoryForm, AddUserForm

# Models
from api.models import Session, FilmCard, Category


# Modelo do usuário custom
User = get_user_model()


@login_required(login_url='user-login')
def session_edit(request, id):
    session = get_object_or_404(Session, id=id)

    if request.method == 'POST':
        form = AddSessionForm(request.POST, instance=session)

        if form.is_valid():
            session = form.save(commit=False)
            session.modified_by = request.user
            session.modified_at = timezone.now()
            session.save()
            messages.success(request, "Sessão alterada com sucesso!")
            return redirect('sessions')

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

    else:
        form = AddSessionForm(instance=session)

    context = {
        'form': form,
        'session': session
    }

    return render(request, 'session/session_edit.html', context)


@login_required(login_url='user-login')
def sessions(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'add_form':
            form = AddSessionForm(request.POST)

            if form.is_valid():
                session = form.save(commit=False)
                session.modified_by = request.user
                session.save()
                messages.success(request, "Nova sessão adicionada com sucesso!")
                return redirect('sessions')

            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)

        if form_type == 'delete_form':
            session_id = request.POST.get('session_id')
            session = get_object_or_404(Session, id=session_id)
            session.delete()
            messages.success(request, "Sessão deletada com sucesso!")

    form = AddSessionForm()
    
    sessions = Session.objects.all()

    context = {
        'form': form,
        'sessions': sessions
    }

    return render(request, 'session/sessions.html', context)


@login_required(login_url='user-login')
def user_edit(request, id):
    user = get_object_or_404(User, id=id)

    if request.method == 'POST':
        form = AddUserForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, "Usuário atualizado com sucesso!")
            return redirect('users')
        
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

    else:
        form = AddUserForm(instance=user)

    context = {
        'user': user,
        'form': form
    }

    return render(request, 'user/user_edit.html', context)


@login_required(login_url='user-login')
def users(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
    
        if form_type == 'add_form':
            form = AddUserForm(request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, "Novo usuário criado com sucesso!")
                return redirect('users')

            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)

        if form_type == 'delete_form':
            user_id = request.POST.get('user_id')

            user = get_object_or_404(User, id=user_id)
            user.delete()
            messages.success(request, "Usuário deletado com sucesso!")
            return redirect('users')

    form = AddUserForm()
    users = User.objects.all()

    context = {
        'form': form,
        'users': users
    }

    return render(request, 'user/users.html', context)


@login_required(login_url='user-login')
def film_edit(request, id):
    film = get_object_or_404(FilmCard, id=id)

    if request.method == 'POST':
        form = AddFilmCardForm(request.POST, request.FILES, instance=film)

        if form.is_valid():
            # Implementar metodo pra mudar a imagem se for atualizada
            film = form.save(commit=False)
            film.modified_by = request.user
            film.modified_at = timezone.now()
            film.save()
            form.save_m2m()

            messages.success(request, "Filme atualizado com sucesso!")
            return redirect('films')

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

    else:
        form = AddFilmCardForm(instance=film)

    context = {
        'film': film,
        'form': form
    }

    return render(request, 'film/film_edit.html', context)


@login_required(login_url='user-login')
def films(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'add_form':
            form = AddFilmCardForm(request.POST, request.FILES)

            if form.is_valid():
                film = form.save(commit=False)
                film.modified_by = request.user
                film.save()
                form.save_m2m()

                messages.success(request, "Novo filme adicionado com sucesso!")
                return redirect('films')
            
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field} {error}')

        if form_type == 'delete_form':
            film_id = request.POST.get('film_id')

            film = get_object_or_404(FilmCard, id=film_id)
            film.thumb_image.delete(save=False)
            film.delete()
            messages.success(request, "Filme deletado com sucesso!")
            return redirect('films')
    
    form = AddFilmCardForm()
    
    films = FilmCard.objects.all()

    context = {
        'form': form,
        'films': films
    }

    return render(request, 'film/films.html', context)


@login_required(login_url='user-login')
def category_edit(request, id):
    category = get_object_or_404(Category, id=id)

    if request.method == 'POST':
        form = AddCategoryForm(request.POST, instance=category)

        if form.is_valid():
            category = form.save(commit=False)
            category.modified_by = request.user
            category.modified_at = timezone.now()
            category.save()
            messages.success(request, "Categoria atualizada com sucesso!")
            return redirect('categories')

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

    else:
        form = AddFilmCardForm(instance=category)

    context = {
        'category': category,
        'form': form
    }

    return render(request, 'category/category_edit.html', context)


@login_required(login_url='user-login')
def categories(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'add_form':
            form = AddCategoryForm(request.POST)
            
            if form.is_valid():
                category = form.save(commit=False)
                category.modified_by = request.user
                category.save()
                messages.success(request, "Nova categoria adicionada com sucesso!")
                return redirect('categories')

            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)

        if form_type == 'delete_form':
            category_id = request.POST.get('category_id')

            category = get_object_or_404(Category, id=category_id)
            category.delete()
            messages.success(request, "Categoria deletada com sucesso!")
            return redirect('categories')

    form = AddCategoryForm()

    categories = Category.objects.all()

    context = {
        'form': form,
        'categories': categories
    }

    return render(request, 'category/categories.html', context)


def user_logout(request):
    logout(request)
    messages.info(request, "Você saiu do sistema!")
    return redirect('user-login')


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(
                request,
                **{User.USERNAME_FIELD: username},
                password=password
            )

            if not user:
                messages.error(request, "Credenciais incorretas!")

            else:
                login(request, user)
                messages.success(request, "Usuário logado com sucesso!")
                return redirect('control-panel')
        
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = UserLoginForm()

    context = {
        'form': form
    }

    return render(request, 'user/user_login.html', context)


@login_required(login_url = 'user-login')
def control_panel(request):
    return render(request, 'control_panel.html')