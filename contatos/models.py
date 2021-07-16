from django.db import models


# Create your models here.


class Grupo(models.Model):
    nome = models.CharField(max_length=50)      # salva campos vazios
    descricao = models.CharField(max_length=200, null=True, blank=True)


class Contato(models.Model):            # nome unico na criação
    nome = models.CharField(max_length=50, unique=True)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    grupos = models.ManyToManyField(Grupo)     # escolher os grupos

    class Meta:
        ordering = ['nome']  # ordenar no banco por nome ordem alfabetica


class Telefone(models.Model):
    numero = models.CharField(max_length=14)
    contato = models.ForeignKey(Contato, on_delete=models.CASCADE)


class Email(models.Model):
    endereco_email = models.EmailField()
    contato = models.ForeignKey(Contato, on_delete=models.CASCADE)


class Endereco(models.Model):
    rua = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    num = models.CharField(max_length=10)
    cep = models.CharField(max_length=9)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    contato = models.ForeignKey(Contato, on_delete=models.CASCADE)
