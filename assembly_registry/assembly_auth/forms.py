from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from assembly_auth.models import Profile
from django.contrib.auth import authenticate


class AssemblyUserAuthenticationForm(AuthenticationForm):
    '''Overwriting the clean function to get lowercase username'''
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            username = username.lower()
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class AssemblyUserCreationForm(UserCreationForm):
    '''Extended user form'''
    email = forms.EmailField(label="Email address", max_length=254, required=True)
    username = forms.CharField(label="Username", max_length=254, required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    organisation = forms.CharField(label='Organisation', required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2", "organisation")

    def clean_username(self):
        '''change username to lowercase'''
        username = self.cleaned_data['username'].lower()
        try:
            User.objects.get(username=username)
            raise forms.ValidationError('A user with that username already exists')
        except User.DoesNotExist:
            return username

    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't create User and Profile without database save")

        user = super(AssemblyUserCreationForm, self).save()
        user_profile = Profile(user=user,
                               organisation=self.cleaned_data['organisation'],
                               )
        user_profile.user = user
        return user_profile
