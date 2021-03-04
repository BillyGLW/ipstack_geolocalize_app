from django.test import TestCase, SimpleTestCase
from django.apps import apps
from django.db import models 
from django.test import Client
from django.contrib.auth.hashers import make_password
import unittest
from unittest import mock
from .models import Geo_Loc, Region
from django.contrib.auth.models import User 
import os
from django.core.management import call_command
from django.urls import reverse_lazy, reverse

test_data_users = [
	{"username":"adam",  "password":"test123"},
	{"username":"adam1", "password":"qwertuqweyz"},
	{"username":"adam2", "password":"testabc"},
	{"username":"adam3", "password":"test12345"},
	{"username":"adam4", "password":"123456798"},
	{"username":"test123", "password":"test12345"}
]
 
test_data_regions = [
	{"continent_name": "Europe", "continent_code": "UE", "country_name": "England", "country_code": "GB", "city": "London", "zip_number": "33-333"},
	{"continent_name": "Europe", "continent_code": "UE", "country_name": "Poland", "country_code": "PL", "city": "WW", "zip_number": "344-323"},
	{"continent_name": "America", "continent_code": "US", "country_name": "US", "country_code": "US", "city": "NY", "zip_number": "01-212"},
	{"continent_name": "Africa", "continent_code": "AM", "country_name": "ABCD", "country_code": "QWER", "city": "XYZ", "zip_number": "99-222"},
	{"continent_name": "XYZ", "continent_code": "AYZ", "country_name": "ABC", "country_code": "FSDOKFKSDFO", "city": "EQWEQWEDS", "zip_number": "33-322"},
	{"continent_name": "WOP", "continent_code": "SAYZ", "country_name": "ZABC", "country_code": "ABOSK", "city": "EQWEQWEDS", "zip_number": "33-6322"},
]

test_data_geoloc = [
	{"ip": "youtube.com", "protocol": "ipv4"},
	{"ip": "onet.pl", "protocol": "ipv6"},
	{"ip": "212.77.98.9", "protocol": "ipv4"},
	{"ip": "212.77.98.9", "protocol": "ipv4"},
	{"ip": "allegro.pl", "protocol": "ipv4"},
	{"ip": "github.com", "protocol": "ipv4"},
	]


class DBRelationsTest(TestCase):

	@classmethod
	def setUpTestData(cls):
		cls._users = []
		for user in test_data_users:
			# https://stackoverflow.com/questions/2619102/djangos-self-client-login-does-not-work-in-unit-tests
			with unittest.mock.patch(__name__ + '.make_password', new=lambda x:x) as patch:
				patch(cls._users.append(User.objects.create(**user)))
		cls._regions = []
		for region in test_data_regions:
			cls._regions.append(Region.objects.create(**region))

		assert len(cls._users) == len(cls._regions)
		cls._geoModels = []
		for i in range(len(cls._users)):
			cls._geoModels.append(Geo_Loc.objects.create(**test_data_geoloc[i], region=cls._regions[i], user=cls._users[i]))
		
		assert len(cls._regions) == len(cls._geoModels)
	
	def test_user_creation(self):
		for i in range(len(self._users)):
			assert self._users[i].username == self._geoModels[i].user.username
		
	def test_db_relations(self):
		for i in range(len(self._users)):
			assert self._geoModels[i]._check_m2m_through_same_relationship() == list()
			assert self._geoModels[i]._check_property_name_related_field_accessor_clashes() == list()
			assert isinstance(self._geoModels[i].user, User) 
			assert isinstance(self._geoModels[i].region, Region) 

class EndpointTest(unittest.TestCase):
	def test_register_endpoint(self):
		client = Client()
		response = client.get('/geoloc/register/')
		assert response.status_code == 200
	def test_login_endpoint(self):
		client = Client()
		response = client.get('/geoloc/login/')
		assert response.status_code == 200
	def test_index_with_redirection_endpoint(self):
		client = Client()
		response = client.get('/geoloc/index/')
		assert response.status_code == 302
		reponse_location = response.get("Location")
		assert ("register" in reponse_location) == True
		
class auth_login_test(DBRelationsTest):

	def test_login_process_via_index(self):
		client = Client()
		for i in range(0, len(self._users)):
			_password = self._users[i].password
			self._users[i].set_password(self._users[i].password)
			self._users[i].save()
			assert client.login(username=self._users[i].username,  password=_password) == True
			response = client.get('/geoloc/index/')
			assert response.status_code == 200

	def test_login_create_process_via_index_JWT(self):
		client = Client()
		_password = self._users[0].password
		self._users[0].set_password(_password)
		self._users[0].save()
		data = {"username": self._users[0].username, "password": _password}
		assert client.login(username=self._users[0].username,  password=_password) == True
		client.logout()
		request = client.post(reverse('geoloc:obtain-new-token'), data=data)
		token = request.data['access']
		header = {'Accept': 'application/json', 'Authorization': 'Bearer ' + token}
		result = client.put('/geoloc/api/v1/create/', content_type="application/json",  HTTP_AUTHORIZATION=header['Authorization'], data={'geo_location': 'wp.pl'})
		assert result.data['created'] == True