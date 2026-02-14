from django import forms
from django.contrib.auth import get_user_model
from api.models import FilmCard, Category

User = get_user_model()


class AddFilmCardForm(forms.ModelForm):
    class Meta:
        model = FilmCard
        fields = ['name', 'category', 'description', 'duration', 'age_control', 'display', 'thumb_url', 'ticket_url']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': "bg-zinc-900 outline-none p-2 rounded-sm",
                'placeholder': "Nome do filme"
            }),
            'description': forms.Textarea(attrs={
                'class': "h-[100px] bg-zinc-900 outline-none p-2 rounded-sm",
                'placeholder': "Descrição do filme..."
            }),
            'category': forms.CheckboxSelectMultiple(attrs={
                'class': ""
            }),
            'duration': forms.NumberInput(attrs={
                'class': "bg-zinc-900 outline-none p-2 rounded-sm",
                'placeholder': "Duração em minutos"
            }),
            'age_control': forms.NumberInput(attrs={
                'class': "bg-zinc-900 outline-none p-2 rounded-sm",
                'placeholder': "Classificação Indicativa"
            }),
            'display': forms.Select(attrs={
                'class': "bg-zinc-900 outline-none p-2 rounded-sm"
            }),
            'thumb_url': forms.URLInput(attrs={
                'class': "w-full bg-zinc-900 outline-none p-2 rounded-sm",
                'placeholder': "Link do banner do filme"
            }),
            'ticket_url': forms.URLInput(attrs={
                'class': "w-full bg-zinc-900 outline-none p-2 rounded-sm",
                'placeholder': "Link de compra de ingressos"
            })
        }

