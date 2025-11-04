from django import forms
from .models import Objeto, Local

class LocalForm(forms.ModelForm):
    class Meta:
        model = Local
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Novo local', 'class': 'input-padrao'}),
        }

class CadastroObjetoForm(forms.ModelForm):
    # Este é um formulário para a seção 'Achou mais um objeto? Cadastre Aqui'
    
    class Meta:
        model = Objeto
        fields = ['nome', 'local_encontrado', 'imagem']
        # Adicionar classes CSS para estilização (opcional, mas bom para o layout)
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'nome', 'class': 'input-padrao'})
        }