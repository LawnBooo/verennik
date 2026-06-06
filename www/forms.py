from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=20, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)