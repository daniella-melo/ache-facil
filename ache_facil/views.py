from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Case, When, Value, IntegerField 
from django.http import Http404
from .models import Objeto, Local, Cor
from .forms import CadastroObjetoForm, LocalForm, CorForm
from fuzzywuzzy import fuzz 

def aplicar_busca_avancada(queryset, query_string):
    if not query_string:
        return queryset

    query_limpa = query_string.strip().lower()
    
    # --- 1. Busca Ampla: Ranquear sobre o queryset inteiro ---
    candidatos = queryset
    
    if not candidatos.exists():
        return queryset.none()
    
    # --- 2. Ranqueamento com FuzzyWuzzy ---

    #score baixo para máxima tolerância.
    RANKEAMENTO_MINIMO = 50 
    resultados_ranqueados = []
    
    for objeto in candidatos:
        nome_local = objeto.local_encontrado.nome if objeto.local_encontrado else ""
        nome_cor = objeto.cor.nome if objeto.cor else ""
        texto_objeto = f"{objeto.nome} {nome_local} {nome_cor}".lower()
        
        score = fuzz.partial_ratio(query_limpa, texto_objeto) 
        
        if score >= RANKEAMENTO_MINIMO:
            resultados_ranqueados.append({'objeto': objeto, 'score': score})
            
    # --- 3. Filtragem Final e Ordenação (Preservando a Ordem do Score) ---
    
    resultados_ranqueados.sort(key=lambda x: x['score'], reverse=True)
    pk_list_ordenada = [item['objeto'].pk for item in resultados_ranqueados]
    
    if not pk_list_ordenada:
        return queryset.none()

    # Preservação da ordem ranqueada
    preservacao_ordem = Case(*[
        When(pk=pk, then=Value(i)) for i, pk in enumerate(pk_list_ordenada)
    ], output_field=IntegerField())

    return queryset.filter(pk__in=pk_list_ordenada).order_by(preservacao_ordem)

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
        
        elif 'cadastrar_cor' in request.POST:
            form_cor = CorForm(request.POST)
            if form_cor.is_valid():
                form_cor.save()
                return redirect('home')
        
        form_objeto = CadastroObjetoForm(request.POST, request.FILES) if 'cadastrar_objeto' in request.POST else CadastroObjetoForm()
    else:
        form_objeto = CadastroObjetoForm()
        
    form_local = LocalForm()
    form_cor = CorForm()
    
    objetos_encontrados = Objeto.objects.all().order_by('-data_cadastro')
    query_atual = request.GET.get('q')
    ordenacao_atual = request.GET.get('ordem', '-data_cadastro')

    status_filter = request.GET.get('status_filter') 
    local_filter = request.GET.get('local_filter')
    cor_filter = request.GET.get('cor_filter')

    if status_filter in ['ACHADO', 'PERDIDO']:
        objetos_encontrados = objetos_encontrados.filter(status=status_filter)

    if local_filter:
        try:
            objetos_encontrados = objetos_encontrados.filter(local_encontrado_id=local_filter)
        except ValueError:
            pass

    if cor_filter:
        try:
            objetos_encontrados = objetos_encontrados.filter(cor_id=cor_filter)
        except ValueError:
            pass

    if query_atual:
        objetos_encontrados = aplicar_busca_avancada(objetos_encontrados, query_atual)
    else:
        objetos_encontrados = objetos_encontrados.order_by(ordenacao_atual)

    locais_disponiveis = Local.objects.all().order_by('nome')
    cores_disponiveis = Cor.objects.all().order_by('nome')


    context = {
        'form_cadastro': form_objeto,
        'form_local': form_local,
        'form_cor': form_cor,
        'objetos_encontrados': objetos_encontrados,
        'query_atual': query_atual,
        'ordenacao_atual': ordenacao_atual,
        'status_atual': status_filter, 
        'locais_disponiveis': locais_disponiveis,
        'cores_disponiveis': cores_disponiveis,
        'local_atual': local_filter,
        'cor_atual': cor_filter,
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
            
            form_cadastro = CadastroObjetoForm()
            form_local = LocalForm()
            form_cor = CorForm()
            contexto = {
                'objeto': objeto,
                'form_edicao': form_edicao, 
                'form_cadastro': form_cadastro, 
                'form_local': form_local,
                'form_cor': form_cor,
                'status_atual': objeto.status, 
            }
            return render(request, 'detalhes.html', contexto)

    form_edicao = CadastroObjetoForm(instance=objeto)
    form_cadastro = CadastroObjetoForm()
    form_local = LocalForm()
    form_cor = CorForm()
    
    contexto = {
        'objeto': objeto,
        'form_edicao': form_edicao,
        'form_cadastro': form_cadastro, 
        'form_local': form_local,
        'form_cor': form_cor,
        'status_atual': objeto.status, 
    }

    return render(request, 'detalhes.html', contexto)