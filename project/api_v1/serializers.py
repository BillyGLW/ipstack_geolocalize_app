from rest_framework import serializers
from geo_loc.models import Geo_Loc, Region
from django.contrib.auth.models import User



class GeoLocationSeriailizer(serializers.ModelSerializer):
	class Meta:
		model = Geo_Loc
		fields = ['id', 'ip', 'protocol', 'region']

class DefaultUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username']



class RegionSeriailizerWithRegions(serializers.ModelSerializer):
	class Meta:
		model = Region
		fields = ['continent_name',
				  'continent_code',
				  'country_name',
				  'country_code',
				  'city',
				  'zip_number',]


class GeoLocationSeriailizerWithRegions(serializers.ModelSerializer):
	region = RegionSeriailizerWithRegions()
	class Meta:
		model = Geo_Loc
		fields = ['ip','protocol','region']

	def create(self, validated_data, **kwargs):
		regions_data = validated_data.pop('region')
		region = Region.objects.create(**regions_data)
		geo_loc = Geo_Loc.objects.create(region=region, **validated_data)
		
		return geo_loc

	def update(self, instance, validated_data,  **kwargs):
		region_data = validated_data.pop('region')
		region = instance.region
		
		instance.ip = validated_data.get('ip', instance.ip)
		instance.protocol = validated_data.get('protocol', instance.protocol)
		instance.protocol = validated_data.get('region', instance.region)
		instance.user = validated_data.get('user', instance.user)
		region.city = region_data.get('continent_name', region.city)
		region.continent_code = region_data.get('continent_code', region.continent_code)
		region.continent_code = region_data.get('continent_code', region.continent_code)
		region.city = region_data.get('city', region.city)
		region.zip_number = region_data.get('zip_number', region.zip_number)

		region.save()
		return instance
