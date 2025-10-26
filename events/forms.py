from django import forms
from .models import Place, Event

class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ['name', 'address', 'city', 'capacity']


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_date', 'end_date', 'place', 'is_published']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
