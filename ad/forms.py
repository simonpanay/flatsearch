from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Street


class FlatAdFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(FlatAdFormHelper, self).__init__(*args, **kwargs)
        self.form_class = 'form-horizontal'
        self.label_class = 'col-sm-2'
        self.field_class = 'col-sm-8'
        self.add_input(Submit('submit', 'Submit'))


class StreetForm(forms.ModelForm):
    class Meta:
        model = Street
        exclude = ('ad',)

    def __init__(self, *args, **kwargs):
        super(StreetForm, self).__init__(*args, **kwargs)
        self.helper = FlatAdFormHelper()
