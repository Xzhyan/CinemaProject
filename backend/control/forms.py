from django import forms
from django.contrib.auth import get_user_model
from api.models import CategoryType, Category, FilmGenre, FilmCard, Session

User = get_user_model()


class AddCategoryTypeForm(forms.ModelForm):
    class Meta:
        model = CategoryType
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': "w-md bg-zinc-900 hover:bg-zinc-700 transition outline-none p-2 rounded-sm shadow-md",
                'placeholder': "Tipo de categoria... ex: Áudio, Vídeo, Idioma..." 
            })
        }


# Atualizar
class AddSessionForm(forms.ModelForm):
    days_list = forms.MultipleChoiceField(
        choices=Session.WEEK_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': "shadow-md"
        }),
        required=True
    )

    film = forms.ModelChoiceField(
        queryset=FilmCard.objects.none(),
        widget=forms.RadioSelect,
        empty_label=None
    )

    class Meta:
        model = Session
        fields = ['name', 'days_list', 'film', 'room']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': "w-full bg-zinc-900 outline-none p-2 rounded-sm shadow-md",
                'placeholder': "Nome da sessão... ex: Sessão 01"
            }),
            'room': forms.TextInput(attrs={
                'class': "w-full bg-zinc-900 outline-none p-2 rounded-sm shadow-md",
                'placeholder': "Sala do filme... ex: Sala 01"
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filtra os filmes que estão na tabela Session
        used_films = Session.objects.values_list('film_id', flat=True)

        # Excluí os filmes já usados do form, para evitar duplicatas
        self.fields['film'].queryset = FilmCard.objects.exclude(id__in=used_films)

    def clean_days_list(self):
        data = self.cleaned_data['days_list']
        return list(data)


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'category_type']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': "bg-zinc-900 outline-none p-2 rounded-sm shadow-md",
                'placeholder': "Nome da categoria"
            }),
            'category_type': forms.Select(attrs={
                'class': "bg-zinc-900 outline-none p-2 rounded-sm shadow-md"
            })
        }


class AddFilmCardForm(forms.ModelForm):
    class Meta:
        model = FilmCard
        fields = ['name', 'film_genre', 'description', 'duration', 'director', 'movie_cast', 'age_rating', 'display', 'thumb_image', 'ticket_url']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': "w-full max-w-68 bg-zinc-900 outline-none p-2 rounded-sm shadow-md",
                'placeholder': "Nome do filme"
            }),
            'film_genre': forms.CheckboxSelectMultiple(attrs={
                'class': "cursor-pointer scale-130 shadow-md"
            }),
            'description': forms.Textarea(attrs={
                'class': "w-xl h-[100px] bg-zinc-900 outline-none p-2 rounded-sm shadow-md",
                'placeholder': "Descrição do filme..."
            }),
            'duration': forms.NumberInput(attrs={
                'class': "w-20 bg-zinc-900 outline-none p-2 rounded-sm shadow-md"
            }),
            'director': forms.TextInput(attrs={
                'class': "w-full bg-zinc-900 outline-none p-2 rounded-sm shadow-md",
                'placeholder': "Nome do diretor do filme"
            }),
            'movie_cast': forms.Textarea(attrs={
                'class': "h-[60px] bg-zinc-900 outline-none p-2 rounded-sm shadow-md",
                'placeholder': "Nomes do elenco do filme separados por vírgula"
            }),
            'age_rating': forms.Select(attrs={
                'class': "bg-zinc-900 outline-none p-2 rounded-sm shadow-md"
            }),
            'display': forms.Select(attrs={
                'class': "bg-zinc-900 outline-none p-2 rounded-sm shadow-md"
            }),
            'thumb_image': forms.FileInput(attrs={
                'class': "w-full bg-zinc-900 outline-none p-2 rounded-sm shadow-md"
            }),
            'ticket_url': forms.URLInput(attrs={
                'class': "w-full bg-zinc-900 outline-none p-2 rounded-sm shadow-md",
                'placeholder': "Link de compra de ingressos"
            })
        }


# ----- User forms -----


class AddUserForm(forms.ModelForm):
    password1 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': "w-full max-w-sm bg-zinc-900 hover:bg-zinc-700 transition outline-none p-2 rounded-sm shadow-md",
            'placeholder': "Digite uma senha"
        })
    )
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': "w-full max-w-sm bg-zinc-900 hover:bg-zinc-700 transition outline-none p-2 rounded-sm shadow-md",
            'placeholder': "Confirme a senha"
        })
    )

    class Meta:
        model = User
        fields = ['username', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': "w-full max-w-sm bg-zinc-900 hover:bg-zinc-700 transition outline-none p-2 rounded-sm shadow-md",
                'placeholder': "Digite o nome de usuário"
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': "cursor-pointer scale-180"
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')

        # Se for o form de criação de usuário.
        if not self.instance.pk:
            if not p1 or not p2:
                raise forms.ValidationError("É obrigatório o uso de senha!")

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("As senhas não coincidem!")
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data['password1']

        # Apénas troca a senha se uma nova for inserida
        if new_password:
            user.set_password(new_password)

        if commit:
            user.save()

        return user
    

class UserLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': "w-full max-w-sm bg-zinc-800 hover:bg-zinc-700 transition outline-none p-2 rounded-sm shadow-md",
            'placeholder': "Digite o nome de usuário"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': "w-full max-w-sm bg-zinc-800 hover:bg-zinc-700 transition outline-none p-2 rounded-sm shadow-md",
            'placeholder': "Digite sua senha de acesso"
        })
    )

    def clean_username(self):
        username = self.cleaned_data['username']

        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("O usuário não existe!")
        
        return username