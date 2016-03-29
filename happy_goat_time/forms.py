
from crispy_forms.layout import Layout, Fieldset, Submit, Field, Div
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from django.contrib.auth.forms import AuthenticationForm as DJAuthenticationForm

from misc.forms import CrispyFormMixin


class AuthenticationForm(CrispyFormMixin, DJAuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)

        self.helper.form_class = ''
        self.helper.label_class = ''
        self.helper.field_class = ''
        self.helper.form_class = 'col-sm-6 col-sm-offset-3'
        self.helper.layout = Layout(
            Div(
                Fieldset(
                    'Login Details',
                    PrependedText('username', '<i class="glyphicon glyphicon-user"></i>'),
                    PrependedText('password', '<i class="glyphicon glyphicon-lock"></i>')
                ),
                Submit('login', 'Login', css_class='btn-lg btn-block')
            , css_class='well well-lg'))
