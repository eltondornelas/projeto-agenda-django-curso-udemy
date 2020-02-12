from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Contato
from django.core.paginator import Paginator
# https://docs.djangoproject.com/en/2.2/topics/pagination/
from django.db.models import Q, Value
# para fazer consultas mais complexas
from django.db.models.functions import Concat
from django.contrib import messages

def index(request):
    # messages.add_message(request, messages.ERROR, 'Ocorreu um Erro!')
    # contatos = Contato.objects.all()  # para passar como chave no dicionário do return
    contatos = Contato.objects.order_by('-id').filter(mostrar=True)  # ordenando na página principal. se tiver o "-" fica em ordem inversa
    # procurar documentação de filter para mais aprofundamento
    
    paginator = Paginator(contatos, 3) # Show 3 contacts per page

    page = request.GET.get('p')  # poderia ser a palavra 'page'
    contatos = paginator.get_page(page)

    return render(request, 'contatos/index.html', {
        'contatos': contatos
    })
    # entenda que o contatos valor ele é os valores contidos no objeto Contato, como se fosse um SELECT


def ver_contato(request, contato_id):
    # try:
    # contato = Contato.objects.get(id=contato_id)  # get, pois só queremos 1 objeto. e dentro do get qual campo está buscando com o argumento
    contato = get_object_or_404(Contato, id=contato_id)

    if not contato.mostrar:
        raise Http404()

    return render(request, 'contatos/ver_contato.html', {
        'contato': contato
    })
    # except Contato.DoesNotExist as e:
        # raise Http404()

def busca(request):
    termo = request.GET.get('termo')  # aqui ele vai pegar o termo escrito no formulário e armazenar na variável

    if termo is None or not termo:  # o or not termo é para verificar que não está vazio, porém vai mostrar o not found
        # raise Http404()
        messages.add_message(request, messages.ERROR, 'Campo termo não pode ficar vazio.')
        # essa mensagem não precisa ter lógica para sumir com ela, pois o Django já faz isso
        return redirect('index')  # nome do view que está em urls.


    campos = Concat('nome', Value(' '), 'sobrenome')

    contatos = Contato.objects.annotate(
        nome_completo = campos
    ).filter(
        Q(nome_completo__icontains=termo) | Q(telefone__icontains=termo)
    )
    
    # contatos = Contato.objects.order_by('-id').filter(
      #  Q(nome__icontains = termo) | Q(sobrenome__icontains = termo),
       # mostrar=True)
    # a forma acima tem um problema, é que se ambos os campos estiverem certo ele vai dizer que não existe

    # print(contatos.query)
    # ordenando na página principal. se tiver o "-" fica em ordem inversa
    # para que a consulta SQL tenha uma "or" ao invés de "and", precisa usar o Q e o | "pipe"

    paginator = Paginator(contatos, 3)  # Show 3 contacts per page

    page = request.GET.get('p')  # poderia ser a palavra 'page'
    contatos = paginator.get_page(page)

    return render(request, 'contatos/busca.html', {
        'contatos': contatos
    })
