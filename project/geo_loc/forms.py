from django import forms

from .models import Geo_Loc, Region

from django.contrib.auth.models import User


class GeoLocUser_Registration(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'password']

		widgets = {
				'password': forms.PasswordInput(),
		}

class GeoLocLookUpData(forms.ModelForm):
	class Meta:
		model = Geo_Loc
		fields = ['ip', 'protocol', 'region']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

class RegionLookUpData(forms.ModelForm):
	class Meta:
		model = Region
		fields = ['continent_name',
				  'continent_code',
				  'country_name',
				  'country_code',
				  'city',
				  'zip_number',]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
