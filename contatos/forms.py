from django import forms
from .models import Contato, Grupo, Telefone, Email, Endereco


class EditarContatoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        contato = Contato.objects.get(id=kwargs.pop('id'))
        self.contato = contato
        super(EditarContatoForm, self).__init__(*args, **kwargs)
        self.fields['nome_contato'] = forms.CharField(max_length=50, initial=contato.nome)
        grupos = Grupo.objects.all()
        grupos_contato = contato.grupos.all()
        for grupo in grupos:
            self.fields[f"g_{grupo.nome}"] = forms.BooleanField(required=False,
                                                                initial=grupo in grupos_contato,
                                                                label=f"{grupo.nome}")

        for i, tel in enumerate(contato.telefone_set.all()):
            self.fields[f"tel_{i}"] = forms.CharField(max_length=14,
                                                      label=f"Telefone {i + 1}",
                                                      initial=contato.telefone_set.all()[i].numero)

        for i, email in enumerate(contato.email_set.all()):
            self.fields[f"email_{i}"] = forms.EmailField(max_length=255,
                                                         label=f"Email {i + 1}",
                                                         initial=contato.email_set.all()[i].endereco_email)

        for endereco in contato.endereco_set.all():
            self.fields["rua"] = forms.CharField(max_length=100,
                                                 initial=endereco.rua)
            self.fields["bairro"] = forms.CharField(max_length=100,
                                                    initial=endereco.bairro)
            self.fields["num"] = forms.CharField(max_length=10,
                                                 initial=endereco.num)
            self.fields["cep"] = forms.CharField(max_length=9,
                                                 initial=endereco.cep)
            self.fields["estado"] = forms.CharField(max_length=100,
                                                    initial=endereco.estado)
            self.fields["cidade"] = forms.CharField(max_length=100,
                                                    initial=endereco.cidade)

    def clean_nome_contato(self):
        nome_contato = self.cleaned_data.get('nome_contato')
        nomes_contatos = []
        for contact in Contato.objects.all():
            nomes_contatos.append(contact.nome)
        nomes_contatos.remove(self.contato.nome)
        if nome_contato in nomes_contatos:
            raise forms.ValidationError("O nome escolhido já está sendo utilizado.")
        return nome_contato


class NovoGrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ('nome', 'descricao')


class NovoTelForm(forms.ModelForm):
    class Meta:
        model = Telefone
        fields = ('numero',)


class NovoEnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ('rua', 'bairro', 'num', 'cep', 'cidade', 'estado')


class NovoEmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ('endereco_email',)


class EditarGrupoForm(forms.Form):
    nome = forms.CharField(max_length=50)
    descricao = forms.CharField(max_length=200, required=False)

    def __init__(self, *args, **kwargs):
        self.grupo = Grupo.objects.get(id=kwargs.pop('id'))
        super(EditarGrupoForm, self).__init__(*args, **kwargs)

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        nome_grupos = []
        for grupo in Grupo.objects.all():
            nome_grupos.append(grupo.nome)
        nome_grupos.remove(self.grupo.nome)
        if nome in nome_grupos:
            raise forms.ValidationError('O nome escolhido já está sendo utilizado')
        else:
            return nome


class NovoContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ('nome', 'photo')
