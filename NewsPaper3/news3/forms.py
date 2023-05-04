from django.forms import ModelForm
from .models import News


class DummyForm(ModelForm):
    class Meta:
        model = News
        fields = ['header', 'description', 'email', 'cat']

