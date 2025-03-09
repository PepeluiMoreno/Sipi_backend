# heritage_defense/rbac/forms.py
# Formularios para la aplicación rbac.
# heritage_defense/rbac/forms.py
# Formularios para la aplicación rbac.

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import Role, UserProfile, UserRole

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ModelChoiceField(queryset=Role.objects.all(), required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'email',
            Row(
                Column('password1', css_class='w-full md:w-1/2 px-2'),
                Column('password2', css_class='w-full md:w-1/2 px-2'),
            ),
            'role',
            Submit('submit', 'Registrar', css_class='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded')
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            role = self.cleaned_data['role']
            UserRole.objects.create(user=user, role=role)
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'date_of_birth', 'profile_picture']