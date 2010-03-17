from django import forms
from django.forms import ModelForm
from catalog.models import AdminUser

class AdminUserForm(ModelForm):
    password = forms.CharField(widget = forms.PasswordInput(render_value=False))

    class Meta:
        model = AdminUser
