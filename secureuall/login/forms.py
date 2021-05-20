from django import forms


class RequestAccessForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'readonly':'readonly'}),
    )
    motive = forms.CharField(
        label="Motive",
        widget=forms.Textarea(attrs={'placeholder': 'Why should you have access to the machine(s)?', 'class': 'form-control', 'rows':5})
    )
