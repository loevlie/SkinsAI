from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Your Name'}),label="")
    from_email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'placeholder':'Email'}),label="")
    message = forms.CharField(required=True,widget=forms.Textarea(attrs={'placeholder':'Message'}),label="")