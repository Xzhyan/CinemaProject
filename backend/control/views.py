from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .forms import AddFilmCardForm
from api.models import FilmCard


def control_panel(request):
    return render(request, 'control_panel.html')


def users(request):
    return render(request, 'users.html')


# Editar filme
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


def categories(request):
    return render(request, 'categories.html')
