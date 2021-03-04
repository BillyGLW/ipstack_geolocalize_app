from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('geoloc/', include(('geo_loc.urls', 'geoloc'), namespace='geoloc')),
    path('', RedirectView.as_view(url=reverse_lazy('geoloc:geo-loc-l_view')))
]
