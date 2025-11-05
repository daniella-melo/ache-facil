from django import forms
from .models import Objeto, Local, Cor

class LocalForm(forms.ModelForm):
    class Meta:
        model = Local
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Novo local', 'class': 'input-padrao'}),
        }

class CorForm(forms.ModelForm):
    class Meta:
        model = Cor
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nova cor', 'class': 'input-padrao'}),
        }

class CadastroObjetoForm(forms.ModelForm):    
    class Meta:
        model = Objeto
        fields = ['nome', 'local_encontrado', 'cor', 'imagem']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'nome', 'class': 'input-padrao'})
        }