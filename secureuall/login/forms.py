from django import forms
from django.core.exceptions import ValidationError
import re
from .models import UserAccessRequest, NotificationType


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


class UserNotificationForm(forms.Form):
    type = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )
    active = forms.BooleanField(required=False)
    value = forms.CharField(
        max_length=300,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )

    def clean_type(self):
        # Make sure that type exists on db
        n = self.cleaned_data['type']
        if not NotificationType.objects.filter(name=n).exists():
            raise ValidationError("Notification type is not valid!", params={'type': n})
        return n

    def clean(self):
        # value is required if active==True
        data = self.cleaned_data
        if data['active'] and not data['value']:
            raise ValidationError("The value is mandatory for active notifications!", params={'value': data['value']})

        # make sure that value matches regex
        type = NotificationType.objects.filter(name=self.cleaned_data['type']).first()
        if data['value'] and data['type']!="Email":
            regex = re.compile(type.regex)
            print(data['value'], regex.fullmatch(data['value']))
            if not regex.fullmatch(data['value']):
                print("INVALID")
                raise ValidationError("Value is not valid for selected type.", params={'value': data['value']})

        return data

