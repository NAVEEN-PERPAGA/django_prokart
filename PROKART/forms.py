from django import forms
from .models import Comments


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ('phones', 'author', 'text', 'created_on')

    def __init__(self, phone_pk=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if phone_pk:
            self.fields['phones'].initial = phone_pk
            # self.fields['phones'].widget = forms.HiddenInput()
