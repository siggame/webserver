from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.bootstrap import FormActions

from .models import BaseClient, TeamClient


password_help = """
<p class="text-info">

Choose a password for cloning and submitting your code. <br>
<span class="text-error">It will be stored inplain text</span>
so that you and your team <br> members will be able
to see it. It can be changed at any time.

</p>
"""


class TeamRepoForm(forms.ModelForm):
    base = forms.ModelChoiceField(queryset=BaseClient.objects.all(),
                                  label="Client Language")
    git_password = forms.CharField(help_text=password_help)
    class Meta:
        model = TeamClient
        fields = ('base', 'git_password')

    def __init__(self, *args, **kwargs):
        # Crispy form styling stuff
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                "Setup your team's code repository",
                'base',
                'git_password',
            ),
            FormActions(
                Submit('submit', 'Submit', css_class='button white')
            )
        )

        # Limit base repo queryset
        base_clients = kwargs.pop('base_clients', None)
        super(TeamRepoForm, self).__init__(*args, **kwargs)
        if base_clients:
            self.fields['base'].queryset = base_clients

    def clean_git_password(self):
        password = self.cleaned_data['git_password']
        if len(password) < 6:
            msg = "Password should be at least 6 characters"
            raise forms.ValidationError(msg)
        return password


class TeamPasswordForm(forms.ModelForm):
    git_password = forms.CharField(help_text=password_help)

    class Meta:
        model = TeamClient
        fields = ('git_password',)

    def __init__(self, *args, **kwargs):
        # Crispy form styling stuff
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                "Change your team's git password",
                'git_password',
            ),
            FormActions(
                Submit('submit', 'Submit', css_class='button white')
            )
        )
        super(TeamPasswordForm, self).__init__(*args, **kwargs)

    def clean_git_password(self):
        password = self.cleaned_data['git_password']
        if len(password) < 6:
            msg = "Password should be at least 6 characters"
            raise forms.ValidationError(msg)
        return password


class AuthForm(forms.Form):
    """Used by the RepoAuthHandler to check data from API clients"""
    teamid = forms.IntegerField()
    password = forms.CharField()
