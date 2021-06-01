from django import forms
from django.core.exceptions import ValidationError

from .models import UserAccessRequest


class RequestAccessForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
    )
    motive = forms.CharField(
        label="Motive",
        widget=forms.Textarea(attrs={'placeholder': 'Why should you have access to the machine(s)?', 'class': 'form-control', 'rows':5})
    )
    role = forms.ChoiceField(
        choices=UserAccessRequest.userType,
        widget=forms.Select(attrs={'class': 'col-12'}),
    )


class UserAccessRequestApprovalForm(forms.Form):
    request = forms.IntegerField(min_value=1)
    approve = forms.BooleanField(required=False)
    notes = forms.CharField(required=False)

    def clean_request(self):
        request = self.cleaned_data['request']
        if not UserAccessRequest.objects.filter(id=request).exists():
            raise ValidationError("Request is not valid!", params={'request': request})
        return request

