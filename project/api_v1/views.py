from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import authentication, permissions
from .serializers import GeoLocationSeriailizer, GeoLocationSeriailizerWithRegions
from geo_loc.models import Geo_Loc
from geo_loc import GeoApi
from django.conf import settings
from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication


class GeoLocationGetView(APIView):
	authentication_classes = [authentication.SessionAuthentication, 
							authentication.BasicAuthentication, 
							authentication.TokenAuthentication,
							JWTAuthentication]
	permission_classes = [permissions.IsAuthenticated]
	http_method_names = ['get']

	def get(self, request, *args, **kwargs):
		context = Geo_Loc.objects.filter(id=kwargs['pk']).all().values()
		return Response(context)

class GeoLocationDeleteView(APIView):
	authentication_classes = [authentication.SessionAuthentication, 
							authentication.BasicAuthentication,
							authentication.TokenAuthentication,
							JWTAuthentication]
	permission_classes = [permissions.IsAuthenticated]
	http_method_names = ['delete']

	def delete(self, request, *args, **kwargs):
		content = dict()
		try:
			context = Geo_Loc.objects.get(id=kwargs['pk']).delete()
			content['deleted'] = True
		except Exception as e:
			content = {'deleted': False, 'error_message': e.__str__()}
		
		return Response(content, status=status.HTTP_404_NOT_FOUND)

class GeoLocationUpdateView(APIView):
	authentication_classes = [authentication.SessionAuthentication, 
							authentication.BasicAuthentication,
							authentication.TokenAuthentication,
							JWTAuthentication]
	permission_classes = [permissions.IsAuthenticated]
	http_method_names = ['put']

	def put(self, request, *args, **kwargs):
		content = dict()
		request.data['id'] = kwargs['pk']
		serializer = GeoLocationSeriailizerWithRegions(instance=Geo_Loc.objects.get(id=kwargs['pk']), 
														data=request.data)
		try:
			if serializer.is_valid():
				serializer.save(user=request.user)
				content['updated'] = True
		except Exception as e:
			content = {'updated': False, 'error_message': e.__str__()}

		return Response(content, status=status.HTTP_200_OK)


class GeoLocationCreateView(APIView):
	authentication_classes = [authentication.SessionAuthentication, 
							authentication.BasicAuthentication,
							authentication.TokenAuthentication,
							JWTAuthentication]
	permission_classes = [permissions.IsAuthenticated]
	http_method_names = ['put']
	

	def put(self, request, *args, **kwargs):
		content = dict()
		serializer = GeoLocationSeriailizerWithRegions(data=request.data if not "geo_location" in request.data 
			else GeoApi(settings.GEO_ACCESS_KEY).get_location(request.data.pop('geo_location')))
		try:
			if serializer.is_valid():
				serializer.save(user=request.user)
				content['created'] = True
		except Exception as e:
			content = {'created': False, 'error_message': e.__str__()}

		return Response(content, status=status.HTTP_200_OK)