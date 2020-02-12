from django.db import models
from contatos.models import Contato
from django import forms


class FormContato(forms.ModelForm):
    class Meta:
        model = Contato
        exclude = ('mostrar',)  # exclui os campos que achar necessário que aparece no formulário. Precisa deixar a vírgula para entender que é uma tupla e não string
    # só com isso já cria um formulário
