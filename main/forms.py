from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from main.models import Person


#Create a new user form
class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'phone', 'email', 'status', 'notes']
        widgets = {
            'status': forms.Select(choices=Person._meta.get_field('status').choices),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

#Super staff sign up/login
class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Require email

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserSignUpForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = None  # Remove helper texts
