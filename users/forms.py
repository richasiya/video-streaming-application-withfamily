from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile


class RegisterForm(UserCreationForm):

    email = forms.EmailField(required=True)
    mobile = forms.CharField(max_length=10, required=True)
    dob = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    # 🔥 Simple password error only
    error_messages = {
        'password_mismatch': 'Password wrong',
    }

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'mobile',
            'dob',
            'password1',
            'password2',
        )


class EditProfileForm(forms.ModelForm):
    bio = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control'}))
    mobile = forms.CharField(required=True, max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    dob = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    avatar = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserProfile
        fields = ('bio', 'mobile', 'dob', 'avatar')

    def clean_mobile(self):
        mobile = (self.cleaned_data.get('mobile') or '').strip()
        if not mobile:
            raise forms.ValidationError('Mobile number is required.')
        if not mobile.isdigit():
            raise forms.ValidationError('Mobile number must contain only digits.')
        if len(mobile) < 10:
            raise forms.ValidationError('Mobile number must be at least 10 digits.')
        return mobile
