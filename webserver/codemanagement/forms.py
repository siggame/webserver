from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.bootstrap import FormActions

from .models import BaseClient, TeamClient


class TeamRepoForm(forms.ModelForm):
    base = forms.ModelChoiceField(queryset=BaseClient.objects.all(),
                                  label="Client Language")
    class Meta:
        model = TeamClient
        fields = ('base',)

    def __init__(self, *args, **kwargs):
        # Crispy form styling stuff
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                "Choose your team's client language",
                'base'
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
