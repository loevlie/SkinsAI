from django import forms
from .models import Comment, Post
from django.contrib.auth.models import User



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password')

        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.TextInput(attrs={'class':'form-control'}),
            'password': forms.TextInput(attrs={'class':'form-control'}),
        }


class ContactForm(forms.Form):
    subject = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Your Name'}),label="")
    from_email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'placeholder':'Email'}),label="")
    message = forms.CharField(required=True,widget=forms.Textarea(attrs={'placeholder':'Message'}),label="")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'slug', 'content')


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'slug', 'content')

