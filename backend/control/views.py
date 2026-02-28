from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from collections import defaultdict

# Forms
from .forms import UserLoginForm, AddUserForm, AddCategoryTypeForm, AddCategoryForm, AddGenreForm, AddFilmCardForm, AddSessionForm

# Models
from api.models import CategoryType, Category, FilmGenre, FilmCard, Session


# Modelo do usuário custom
User = get_user_model()


@login_required(login_url='user-login')
def session_edit(request, id):
    session = get_object_or_404(Session, id=id)

    if request.method == 'POST':
        form = AddSessionForm(request.POST, instance=session)

        if form.is_valid():
            categories = request.POST.getlist('categories')

            session = form.save(commit=False)
            session.modified_by = request.user
            session.modified_at = timezone.now()
            session.save()

            session.categories.set(request.POST.getlist('categories'))

            messages.success(request, "Sessão alterada com sucesso!")
            return redirect('sessions')

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

    else:
        form = AddSessionForm(instance=session)

    categories = Category.objects.all()

    grouped_catgs = defaultdict(list)

    for catg in categories:
        grouped_catgs[catg.category_type].append(catg)

    grouped_catgs = dict(grouped_catgs)

    context = {
        'form': form,
        'session': session,
        'grouped_catgs': grouped_catgs
    }

    return render(request, 'session/session_edit.html', context)


@login_required(login_url='user-login')
def sessions(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'add_form':
            form = AddSessionForm(request.POST)

            if form.is_valid():
                categories = request.POST.getlist('categories')
                
                session = form.save(commit=False)
                session.modified_by = request.user
                session.modified_at = timezone.now()
                session.save()

                session.categories.set(request.POST.getlist('categories'))

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
    categories = Category.objects.all()

    grouped_catgs = defaultdict(list)

    for catg in categories:
        grouped_catgs[catg.category_type].append(catg)

    grouped_catgs = dict(grouped_catgs)

    context = {
        'form': form,
        'sessions': sessions,
        'grouped_catgs': grouped_catgs
    }

    return render(request, 'session/sessions.html', context)


@login_required(login_url='user-login')
def genre_edit(request, id):
    genre = get_object_or_404(FilmGenre, id=id)

    if request.method == 'POST':
        form = AddGenreForm(request.POST, instance=genre)
        if form.is_valid():
            genre = form.save(commit=False)
            genre.modified_by = request.user
            genre.modified_at = timezone.now()
            genre.save()

            messages.success(request, "Gênero modificado com sucesso!")
            return redirect('genres')
        
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

    else:
        form = AddGenreForm(instance=genre)

    context = {
        'form': form,
        'genre': genre
    }

    return render(request, 'film/genre_edit.html', context)


@login_required(login_url='user-login')
def genres(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'add_form':
            form = AddGenreForm(request.POST)
            if form.is_valid():
                genre = form.save(commit=False)
                genre.modified_by = request.user
                genre.modified_at = timezone.now()
                genre.save()
                
                messages.success(request, "Novo gênero adicionado com sucesso!")
                return redirect('genres')

            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)

        if form_type == 'delete_form':
            genre_id = request.POST.get('genre_id')
            genre = get_object_or_404(FilmGenre, id=genre_id)
            genre.delete()
            messages.success(request, "Gênero deletado com sucesso!")
            return redirect('genres')

    form = AddGenreForm()
    genres = FilmGenre.objects.all()

    context = {
        'form': form,
        'genres': genres
    }

    return render(request, 'film/genres.html', context)


@login_required(login_url='user-login')
def film_edit(request, id):
    film = get_object_or_404(FilmCard, id=id)

    if request.method == 'POST':
        old_thumb_img = film.thumb_image # Imagem antiga do filme
        form = AddFilmCardForm(request.POST, request.FILES, instance=film)

        if form.is_valid():
            film = form.save(commit=False)
            film.modified_by = request.user
            film.modified_at = timezone.now()
            film.save()
            form.save_m2m()

            # Apaga a imagem antiga, se for alterada
            if 'thumb_image' in request.FILES and old_thumb_img:
                old_thumb_img.delete(save=False)

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

    
    form = AddCategoryForm(instance=category)

    context = {
        'form': form,
        'category': category
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


def catg_type_edit(request, id):
    c_type = get_object_or_404(CategoryType, id=id)

    if request.method == 'POST':
        form = AddCategoryTypeForm(request.POST, instance=c_type)

        if form.is_valid():
            c_type = form.save(commit=False)
            c_type.modified_by = request.user
            c_type.modified_at = timezone.now()
            c_type.save()
            messages.success(request, "Tipo de categoria atualizada com sucesso!")
            return redirect('catg-types')

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    
    else:
        form = AddCategoryTypeForm(instance=c_type)

    context = {
        'form': form,
        'c_type': c_type
    }

    return render(request, 'category/catg_type_edit.html', context)


def catg_type(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'add_form':
            form = AddCategoryTypeForm(request.POST)

            if form.is_valid:
                c_type = form.save(commit=False)
                c_type.modified_by = request.user
                c_type.save()
                messages.success(request, "Novo tipo de categoria adicionada com sucesso!")
                return redirect('catg-types')

            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)

        if form_type == 'delete_form':
            c_type_id = request.POST.get('c_type_id')
            c_type = get_object_or_404(CategoryType, id=c_type_id)
            c_type.delete()
            messages.success(request, "Tipo de categoria deletada com sucesso!")
            return redirect('catg-types')

    else:
        form = AddCategoryTypeForm()
        c_types = CategoryType.objects.all()


    context = {
        'form': form,
        'c_types': c_types
    }
    
    return render(request, 'category/catg_type.html', context)


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
