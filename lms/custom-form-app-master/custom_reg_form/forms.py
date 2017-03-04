from .models import ExtraInfo
from django.forms import ModelForm

class ExtraInfoForm(ModelForm):
    """
    The fields on this form are derived from the ExtraInfo model in models.py.
    """
    def __init__(self, *args, **kwargs):
        super(ExtraInfoForm, self).__init__(*args, **kwargs)
        self.fields['confirm_password'].error_messages = {
            "required": u"enter password again",
            "invalid": u"These passwords don't match. Try again?",
        }

    class Meta(object):
        model = ExtraInfo
        fields = 'confirm_password'

