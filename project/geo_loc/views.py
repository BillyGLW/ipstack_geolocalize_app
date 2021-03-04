from django.views.generic.edit import (CreateView, DeleteView,
										UpdateView)
from django.shortcuts import render, get_object_or_404, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView
from .models import Geo_Loc, Region
from .geoapi import GeoApi
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from django.http import HttpResponseNotFound
from django.views.generic.base import RedirectView
from django.contrib.auth.forms import UserCreationForm
from .forms import (GeoLocUser_Registration, GeoLocLookUpData,
					RegionLookUpData)

class GeoLocRegisterCreateView(CreateView):
	model = User
	form_class = UserCreationForm
	
	def post(self, *args, **kwargs):
		super().post(*args, **kwargs)
		user = authenticate(username=self.request.POST['username'],
		 password=self.request.POST['password1'])
		if user is not None or 'AnonymousUser':
			login(self.request, user)
			return HttpResponseRedirect(reverse('geoloc:geo-loc-l_view'))
		return HttpResponseRedirect(reverse('geoloc:geo-loc-c_view'))

	def get_success_url(self):
		pk = self.object.id
		post_instance = get_object_or_404(User, pk=pk)
		return reverse('geoloc:geo-loc-l_view')

class GeoLocUpdateView(UpdateView):
	model = Region
	success_url = reverse_lazy('geoloc:geo-loc-l_view')
	fields = ['continent_name',
		  'continent_code',
		  'country_name',
		  'country_code',
		  'city',
		  'zip_number',]

class GeoLocDeleteView(DeleteView):
	model = Geo_Loc
	success_url = reverse_lazy('geoloc:geo-loc-l_view')

class GeoLocLookUpCreateView(CreateView):
	model = Geo_Loc

	def post(self, *args, **kwargs):
		key = settings.GEO_ACCESS_KEY
		g_api  = GeoApi(key)
		geo_locations_data = g_api.get_location(self.request.POST['geo_ip'])

		form = GeoLocLookUpData(geo_locations_data)
		form_region = RegionLookUpData(geo_locations_data.pop('region'))

		if form.is_valid() and form_region.is_valid():
			geo_loc_data = form.save()
			form_geo_data = form_region.save()
			geo_loc_data.user = self.request.user
			geo_loc_data.region = form_geo_data
			geo_loc_data.save()
			form_geo_data.save()
			return HttpResponseRedirect(reverse('geoloc:geo-loc-l_view'))
		raise Http404('Form validation was not possible.')

	def get_success_url(self):
		pk = self.object.id
		post_instance = get_object_or_404(User, pk=pk)
		return reverse('geoloc:geo-loc-l_view')


class GeoLocListView(LoginRequiredMixin, ListView):
	model = Geo_Loc
	paginate_by = 5

	def post(self, request, *args, **kwargs):
	    self.object_list = self.get_queryset()
	    allow_empty = self.get_allow_empty()

	    if not allow_empty:
	        if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
	            is_empty = not self.object_list.exists()
	        else:
	            is_empty = not self.object_list
	        if is_empty:
	            raise Http404(_('Empty list and “%(class_name)s.allow_empty” is False.') % {
	                'class_name': self.__class__.__name__,
	            })
	    context = self.get_context_data()
	    return self.render_to_response(context)

	def get_context_data(self, *, object_list=None, **kwargs):
		queryset = object_list if object_list is not None else self.object_list
		return super().get_context_data(
            object_list=queryset.filter(user=self.request.user),
            geo_ip_lookup=self.request.POST['geo_ip'] if "geo_ip" in self.request.POST
             else self.request.META.get("REMOTE_ADDR"),
            **kwargs)


class GeoLocLoginView(LoginView):
	model = User

	def get_succes_url(self):
		return reverse("geoloc:geo-loc-l_view")

class GeoLocLogoutView(LogoutView):
	model = User