from django.forms import ModelForm
from .models import Hotel


class HotelForm(ModelForm):
    class Meta:
        model = Hotel
        fields = '__all__'
