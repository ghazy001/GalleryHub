from django import forms
from .models import Category, Article

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug']


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'title',
            'slug',
            'category',
            'summary',
            'body',
            'is_published',
            'published_at',
            'cover_image',
            # cover_image is not included here yet because handling file upload
            # needs enctype="multipart/form-data". We’ll wire that later if you want images.
        ]
        widgets = {
            'published_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'body': forms.Textarea(attrs={'rows': 6}),
            'summary': forms.Textarea(attrs={'rows': 3}),
        }
