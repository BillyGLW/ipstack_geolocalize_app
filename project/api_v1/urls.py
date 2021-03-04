from django.urls import path, reverse_lazy, include

from .views import (GeoLocationGetView, GeoLocationDeleteView, GeoLocationCreateView, GeoLocationUpdateView)
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
		path('get/<int:pk>/', GeoLocationGetView.as_view()),
		path('delete/<int:pk>/', GeoLocationDeleteView.as_view()),
		path('create/', GeoLocationCreateView.as_view()),
		path('update/<int:pk>/', GeoLocationUpdateView.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)