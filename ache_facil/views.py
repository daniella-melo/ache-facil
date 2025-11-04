from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q 
from django.http import Http404
from .models import Objeto, Local
from .forms import CadastroObjetoForm, LocalForm

def home(request):
    if request.method == 'POST':
        if 'cadastrar_objeto' in request.POST:
            form_objeto = CadastroObjetoForm(request.POST, request.FILES)
            if form_objeto.is_valid():
                form_objeto.save() 
                return redirect('home')
        
        elif 'cadastrar_local' in request.POST:
            form_local = LocalForm(request.POST)
            if form_local.is_valid():
                form_local.save()
                return redirect('home')
        
        form_objeto = CadastroObjetoForm()
    else:
        form_objeto = CadastroObjetoForm()

    form_local = LocalForm()

    objetos_encontrados = Objeto.objects.all().order_by('-data_cadastro')
    query_atual = request.GET.get('q')
    ordenacao_atual = request.GET.get('ordem', '-data_cadastro')
    status_filter = request.GET.get('status_filter') 

    if status_filter in ['ACHADO', 'PERDIDO']:
        objetos_encontrados = objetos_encontrados.filter(status=status_filter)

    if query_atual:
        objetos_encontrados = objetos_encontrados.filter(
            Q(nome__icontains=query_atual) | 
            Q(local_encontrado__icontains=query_atual)
        )

    objetos_encontrados = objetos_encontrados.order_by(ordenacao_atual)

    context = {
        'form_cadastro': form_objeto,
        'form_local': form_local,
        'objetos_encontrados': objetos_encontrados,
        'query_atual': query_atual,
        'ordenacao_atual': ordenacao_atual,
        'status_atual': status_filter, 
    }

    return render(request, 'home.html', context)

def detalhes_objeto(request, pk):
    objeto = get_object_or_404(Objeto, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'marcar_achado':
            objeto.status = 'ACHADO'
            objeto.save()
            return redirect('detalhes_objeto', pk=objeto.pk)

        elif action == 'marcar_perdido':
            objeto.status = 'PERDIDO'
            objeto.save()
            return redirect('detalhes_objeto', pk=objeto.pk)

        elif action == 'excluir':
            objeto.delete()
            return redirect('home')
            
        elif action == 'salvar_edicao':
            form_edicao = CadastroObjetoForm(request.POST, request.FILES, instance=objeto)
            
            if form_edicao.is_valid():
                form_edicao.save()
                return redirect('detalhes_objeto', pk=objeto.pk)
            
            contexto = {
                'objeto': objeto,
                'form_edicao': form_edicao, 
                'form_cadastro': CadastroObjetoForm(),
                'status_atual': objeto.status, 
            }
            return render(request, 'detalhes.html', contexto)

    form_edicao = CadastroObjetoForm(instance=objeto)
    form_cadastro = CadastroObjetoForm()
    form_local = LocalForm()
    
    contexto = {
        'objeto': objeto,
        'form_edicao': form_edicao,
        'form_cadastro': form_cadastro, 
        'form_local': form_local,
        'status_atual': objeto.status, 
    }

    return render(request, 'detalhes.html', contexto)