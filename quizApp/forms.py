from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


from .models import QuizModel, Quiz


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already in use.')
        return email



class QuizModelForm(ModelForm):
    class Meta:
        model = QuizModel
        fields = ['question','option1','option2','option3','option4','ans']

class CreateQuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ['name']

class SearchForm(forms.Form):
    query = forms.CharField()
