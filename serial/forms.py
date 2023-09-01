from django import forms
from .models import Episode

class EpisodeSelectionForm(forms.Form):
    episode = forms.ModelChoiceField(queryset=Episode.objects.all(), empty_label=None)
