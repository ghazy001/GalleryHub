from django import forms
from .models import Artwork, ArtworkFeedback

class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class ArtworkFeedbackForm(forms.ModelForm):
    class Meta:
        model = ArtworkFeedback
        fields = [
            'artwork',
            'user',
            'name',
            'comment',
            'rating',
            'is_approved',
        ]
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }
