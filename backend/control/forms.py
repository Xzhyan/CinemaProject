from django import forms
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from api.models import Session, Category, FilmCard

User = get_user_model()


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
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': "bg-zinc-900 outline-none p-2 rounded-sm shadow-md",
                'placeholder': "Nome da categoria"
            })
        }


class AddFilmCardForm(forms.ModelForm):
    class Meta:
        model = FilmCard
        fields = ['name', 'category', 'description', 'duration', 'age_rating', 'display', 'thumb_image', 'ticket_url']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': "w-full max-w-68 bg-zinc-900 outline-none p-2 rounded-sm shadow-md",
                'placeholder': "Nome do filme"
            }),
            'description': forms.Textarea(attrs={
                'class': "h-[100px] bg-zinc-900 outline-none p-2 rounded-sm shadow-md",
                'placeholder': "Descrição do filme..."
            }),
            'category': forms.CheckboxSelectMultiple(attrs={
                'class': "shadow-md"
            }),
            'duration': forms.NumberInput(attrs={
                'class': "w-20 bg-zinc-900 outline-none p-2 rounded-sm shadow-md"
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


class AddUserForm(forms.ModelForm):
    password1 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': "w-full max-w-sm bg-zinc-900 outline-none p-2 rounded-sm shadow-md",
            'placeholder': "Digite uma senha"
        })
    )
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': "w-full max-w-sm bg-zinc-900 outline-none p-2 rounded-sm shadow-md",
            'placeholder': "Confirme a senha"
        })
    )

    class Meta:
        model = User
        fields = ['username', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': "w-full max-w-sm bg-zinc-900 outline-none p-2 rounded-sm shadow-md",
                'placeholder': "Digite o nome de usuário"
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': "scale-180"
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
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

        return user
    

class UserLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': "w-full max-w-sm bg-zinc-800 outline-none p-2 rounded-sm shadow-md",
            'placeholder': "Digite o nome de usuário"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': "w-full max-w-sm bg-zinc-800 outline-none p-2 rounded-sm shadow-md",
            'placeholder': "Digite sua senha de acesso"
        })
    )

    def clean_username(self):
        username = self.cleaned_data['username']

        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("O usuário não existe!")
        
        return username