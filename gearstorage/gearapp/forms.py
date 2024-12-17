from django import forms
from .models import Mission
from datetime import datetime



class MissionForm(forms.ModelForm):
    class Meta:
        model =Mission

        fields = [
            "title",
            "date_start",
            "duration",
            "description",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date_start"] = forms.DateField(widget=forms.SelectDateWidget)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
