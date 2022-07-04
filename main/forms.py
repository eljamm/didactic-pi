from django import forms


class AddSensor(forms.Form):
    name = forms.CharField(label="Name", max_length=150)


class AddData(forms.Form):
    sensor_id = forms.IntegerField(label="ID")
    data = forms.CharField(label="Data", max_length=300)
