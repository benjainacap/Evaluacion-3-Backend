from django import forms
from inscripcion_APP.models import Inscripcion

class FormInscripcion(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = '__all__'