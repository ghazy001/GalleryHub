from django import forms

class ImageGenerateForm(forms.Form):
    prompt = forms.CharField(
        label="Describe the image you want",
        widget=forms.Textarea(attrs={
            "placeholder": "a cyberpunk cat hacking a computer, neon lighting, 4k",
            "rows": 3,
            "class": "form-control",
        })
    )


class BackgroundRemoveForm(forms.Form):
    image = forms.ImageField(
        label="Upload an image to remove its background",
        widget=forms.ClearableFileInput(attrs={
            "class": "form-control",
        })
    )


class ImageEditorForm(forms.Form):
    image = forms.ImageField(
        label="Upload image to edit",
        required=True,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )
    text = forms.CharField(
        label="Describe the edit you want",
        required=True,
        widget=forms.Textarea(attrs={
            "placeholder": "Make it look like a cinematic sci-fi movie poster with neon lighting",
            "rows": 3,
            "class": "form-control",
        })
    )





