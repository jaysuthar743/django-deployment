from django import forms
from django.core import validators
from django.contrib.auth.models import User
from first_app.models import UserProfileInfo


def check_for_z(value):
    if value[0].lower() !='z':
        raise forms.ValidationError("Name Need to Start with Z")

class FormName(forms.Form):
    name = forms.CharField() # validators=[check_for_z]
    email = forms.EmailField()
    verify_email = forms.EmailField(label='Enter you Email Again')
    text = forms.CharField(widget = forms.Textarea)
    botcatcher  = forms.CharField(required=False,
                                  widget=forms.HiddenInput,
                                  validators=[validators.MaxLengthValidator(0)])

    #  cleam particular field make a function named clean_<fieldname>
    # def clean_botcatcher(self):
    #     botcatcher = self.cleaned_data['botcatcher']
    #     if len(botcatcher) > 0:
    #         raise forms.ValidationError("GOTCHA BOT!!")
    #     return botcatcher
    # clean entire form

    def clean(self):
        all_clean_data = super().clean()
        email = all_clean_data['email']
        vmail = all_clean_data['verify_email']
        if email != vmail:
            raise forms.ValidationError("Make Sure Email Match")

class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)
    class Meta():
        model = User
        fields = ('username', 'email', 'password')

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site', 'profile_pic')
