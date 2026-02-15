from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .forms import AddFilmCardForm, AddCategoryForm
from api.models import FilmCard, Category


def control_panel(request):
    return render(request, 'control_panel.html')


def users(request):
    return render(request, 'users.html')


def film_edit(request, id):
    film = get_object_or_404(FilmCard, id=id)

    if request.method == 'POST':
        form = AddFilmCardForm(request.POST, instance=film)

        if form.is_valid():
            form.save()
            messages.success(request, "Filme atualizado com sucesso!")
            return redirect('films')

    else:
        form = AddFilmCardForm(instance=film)

    context = {
        'film': film,
        'form': form
    }

    return render(request, 'film_edit.html', context)


def films(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type') # Tipo do formulario

        # Adicionar novo filme
        if form_type == 'add_form':
            form = AddFilmCardForm(request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, "Novo filme adicionado com sucesso!")
                return redirect('films')
            
            else:
                messages.error(request, "Formulário inválido!")
        
        # Deletar filme
        if form_type == 'delete_form':
            film_id = request.POST.get('film_id')

            film = get_object_or_404(FilmCard, id=film_id)
            film.delete()
            messages.success(request, "Filme deletado com sucesso!")
            return redirect('films')
    
    form = AddFilmCardForm()
    
    films = FilmCard.objects.all()

    context = {
        'form': form,
        'films': films
    }

    return render(request, 'films.html', context)


def category_edit(request, id):
    category = get_object_or_404(Category, id=id)

    if request.method == 'POST':
        form = AddCategoryForm(request.POST, instance=category)

        if form.is_valid():
            form.save()
            messages.success(request, "Categoria atualizada com sucesso!")
            return redirect('categories')

    else:
        form = AddFilmCardForm(instance=category)

    context = {
        'category': category,
        'form': form
    }

    return render(request, 'category_edit.html', context)


def categories(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'add_form':
            form = AddCategoryForm(request.POST)
            
            if form.is_valid():
                form.save()
                messages.success(request, "Nova categoria adicionada com sucesso!")
                return redirect('categories')

            else:
                messages.error(request, "Formulário inválido!")

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

    return render(request, 'categories.html', context)
