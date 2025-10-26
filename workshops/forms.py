from django import forms
from .models import Workshop, Material

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = [
            'name',
            'description',
            'stock_quantity',
            'unit',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class WorkshopForm(forms.ModelForm):
    class Meta:
        model = Workshop
        fields = [
            'title',
            'instructor',
            'description',
            'place',
            'start_time',
            'end_time',
            'capacity',
            'is_active',
            'materials',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
