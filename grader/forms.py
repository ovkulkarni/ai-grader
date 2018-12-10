from django.forms import ModelForm
from .models import Submission


class SubmissionForm(ModelForm):
    class Meta:
        model = Submission
        fields = ['lab', 'code']
