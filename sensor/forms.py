from django import forms


class AddRaspi(forms.Form):
    name = forms.CharField(label="name", max_length=150)
    address = forms.GenericIPAddressField(label="address")
