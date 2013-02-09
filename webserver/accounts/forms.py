from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Button, HTML, Field
from crispy_forms.bootstrap import FormActions

from models import UserProfile


# Create the form class.
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()


    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                'Update Profile',
                'first_name',
                'last_name',
                'email',
                HTML('<hr>'),
                Field('about_me', placeholder="Tell us about yourself!"),
                ),
            FormActions(
                Submit('save', 'Save changes'),
                Button('cancel', 'Cancel')
                ),
            )


    def save(self, *args, **kwargs):
        profile = super(UserProfileForm, self).save(*args, **kwargs)
        profile.user.first_name = self.cleaned_data['first_name']
        profile.user.last_name = self.cleaned_data['last_name']
        profile.user.email = self.cleaned_data['email']
        profile.user.save(*args, **kwargs)
        print "Saved"
        return profile
