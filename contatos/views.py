from django.shortcuts import render, get_object_or_404, redirect
from .models import Contato, Grupo, Telefone, Email, Endereco
from .forms import EditarContatoForm, NovoGrupoForm, NovoTelForm, NovoEmailForm, EditarGrupoForm, NovoContatoForm, NovoEnderecoForm
from rest_framework import viewsets
from .serializers import ContatoSerializer


def contatos_list_view(request, grupo_id=None):
    grupo = None
    busca = None
    if grupo_id:
        grupo = get_object_or_404(Grupo, id=grupo_id)
        contatos = grupo.contato_set.all()
    elif request.POST.get('busca'):
        busca = request.POST.get('busca')
        contatos = Contato.objects.filter(nome__contains=busca)
    else:
        contatos = Contato.objects.all()
    return render(request, 'contatos/contatos_list.html', {'contatos': contatos, 'grupo': grupo, 'busca': busca})


def editar_contato(request, contato_id):
    contato = get_object_or_404(Contato, id=contato_id)
    if request.method == 'POST':
        form = EditarContatoForm(request.POST, id=contato_id)
        if form.is_valid():
            cd = form.cleaned_data
            endereco = Endereco.objects.get(contato_id=contato.id)
            endereco.rua = cd['rua']
            endereco.cep = cd['cep']
            endereco.bairro = cd['bairro']
            endereco.num = cd['num']
            endereco.estado = cd['estado']
            endereco.cidade = cd['cidade']
            contato.nome = cd['nome_contato']
            contato.save()
            endereco.save()

            cd_grupos = []
            cd_tels = []
            cd_emails = []

            for nome, valor in cd.items():
                if nome.startswith('tel_'):
                    cd_tels.append(valor)
                elif nome.startswith('email_'):
                    cd_emails.append(valor)
                elif nome.startswith('g_'):
                    if valor:
                        grupo = Grupo.objects.get(nome=nome.replace('g_', ''))
                        cd_grupos.append(grupo)

            contato_tels = contato.telefone_set.all()
            contato_emails = contato.email_set.all()
            contato_grupos = contato.grupos.all()

            for i, tel in enumerate(contato_tels):
                tel.numero = cd_tels[i]
                tel.save()

            for i, email in enumerate(contato_emails):
                email.endereco = cd_emails[i]
                email.save()

            for grupo in cd_grupos:
                if grupo in contato.grupos.all():
                    pass
                else:
                    contato.grupos.add(grupo)

            for grupo in contato_grupos:
                if grupo in cd_grupos:
                    pass
                else:
                    contato.grupos.remove(grupo)

            return redirect('contatos_list_view')
    else:
        form = EditarContatoForm(id=contato_id)
    return render(request, 'contatos/editar_contato.html', {'form': form, 'contato': contato})


def novo_grupo_view(request):
    if request.method == 'POST':
        form = NovoGrupoForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('contatos_list_view')
    else:
        form = NovoGrupoForm()
    return render(request, 'contatos/novo_grupo.html', {'form': form})


def novo_tel_view(request, contato_id):
    contato = get_object_or_404(Contato, id=contato_id)
    if request.method == 'POST':
        form = NovoTelForm(data=request.POST)
        if form.is_valid():
            novo_tel = form.save(commit=False)
            novo_tel.contato = contato
            novo_tel.save()
            return redirect('editar_contato', contato_id=contato.id)
    else:
        form = NovoTelForm()
    return render(request, 'contatos/novo_tel.html', {'form': form, 'contato': contato})


def novo_endereco_view(request, contato_id):
    contato = get_object_or_404(Contato, id=contato_id)
    if request.method == 'POST':
        form = NovoEnderecoForm(data=request.POST)
        if form.is_valid():
            novo_endereco = form.save(commit=False)
            novo_endereco.contato = contato
            novo_endereco.save()
            return redirect('editar_contato', contato_id=contato.id)
    else:
        form = NovoEnderecoForm()
    return render(request, 'contatos/novo_endereco.html', {'form': form, 'contato': contato})


def novo_email_view(request, contato_id):
    contato = get_object_or_404(Contato, id=contato_id)
    if request.method == 'POST':
        form = NovoEmailForm(data=request.POST)
        if form.is_valid():
            novo_email = form.save(commit=False)
            novo_email.contato = contato
            novo_email.save()
            return redirect('editar_contato', contato_id=contato.id)
    else:
        form = NovoEmailForm()
    return render(request, 'contatos/novo_email.html', {'form': form, 'contato': contato})


def excluir_contato_view(request, contato_id):
    contato = get_object_or_404(Contato, id=contato_id)
    contato.delete()
    return redirect('contatos_list_view')


def excluir_telefone_view(request, contato_id, label):
    contato = get_object_or_404(Contato, id=contato_id)
    telefone_seq = int(label.replace('Telefone ', '')) - 1
    telefones_contato = Telefone.objects.filter(contato=contato)
    telefone = telefones_contato[telefone_seq]
    telefone.delete()
    return redirect('editar_contato', contato_id=contato.id)


def excluir_email_view(request, contato_id, label):
    contato = get_object_or_404(Contato, id=contato_id)
    email_seq = int(label.replace('Email ', '')) - 1
    emails_contato = Email.objects.filter(contato=contato)
    email = emails_contato[email_seq]
    email.delete()
    return redirect('editar_contato', contato_id=contato.id)


def grupos_list_view(request):
    grupos = Grupo.objects.all()
    return render(request, 'contatos/grupos_list.html', {'grupos': grupos})


def editar_grupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, id=grupo_id)
    if request.method == 'POST':
        form = EditarGrupoForm(data=request.POST, id=grupo.id)
        if form.is_valid():
            cd = form.cleaned_data
            grupo.nome = cd['nome']
            grupo.descricao = cd['descricao']
            grupo.save()
            return redirect('grupos_list')
    else:
        form = EditarGrupoForm(initial={'nome': grupo.nome, 'descricao': grupo.descricao}, id=grupo_id)
    return render(request, 'contatos/editar_grupo.html', {'grupo': grupo, 'form': form})


def excluir_grupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, id=grupo_id)
    grupo.delete()
    return redirect('grupos_list')


def novo_contato_view(request):
    if request.method == "POST":
        form = NovoContatoForm(request.POST, request.FILES,)
        if form.is_valid():
            novo_contato = form.save()
            return redirect('editar_contato', contato_id=novo_contato.id)
    else:
        form = NovoContatoForm()
    return render(request, 'contatos/novo_contato.html', {'form': form})


class ContatoViewSet(viewsets.ModelViewSet):
    queryset = Contato.objects.all()
    serializer_class = ContatoSerializer
