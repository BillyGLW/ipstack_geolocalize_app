from django.db import models
from django.contrib.auth.models import User

class Region(models.Model):
	continent_name = models.CharField(max_length=50, unique=False)
	continent_code = models.CharField(max_length=50, unique=False)
	country_name = models.CharField(max_length=50, unique=False)
	country_code = models.CharField(max_length=50, unique=False)
	city = models.CharField(max_length=50, unique=False)
	zip_number = models.CharField(max_length=10, unique=False)

	def __str__(self):
		return f'{self.city}'


class Geo_Loc(models.Model):
	ip = models.CharField(max_length=50, unique=False)
	protocol = models.CharField(max_length=50, unique=False)
	region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True, related_name="geo_loc_region")
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="geo_loc_user")

	def __str__(self):
		return f'{self.ip} {self.protocol}'

