from django import forms
from .models import Menu


class MenuParentForm(forms.Form):
    page = forms.ModelChoiceField(queryset=Menu.objects.all(), to_field_name='title')

    def label_from_instance(self, obj):
        return 'My Object #%i' % obj.id
