from django.urls import path, reverse_lazy, include

from .views import (GeoLocListView, GeoLocRegisterCreateView,
					 GeoLocLoginView, GeoLocLogoutView,
					 GeoLocLookUpCreateView, GeoLocDeleteView,
					 GeoLocUpdateView
					 )
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
		path('index/', GeoLocListView.as_view(), name='geo-loc-l_view'),
		path('index/lookup/', GeoLocLookUpCreateView.as_view(), name='geo-loc-lu_view'),
		path('register/', GeoLocRegisterCreateView.as_view(), name='geo-loc-c_view'),
		path('login/', GeoLocLoginView.as_view(), name='geo-loc-login_view'),
		path('logout/', GeoLocLogoutView.as_view(), name='geo-loc-logout_view'),
		# CRUD
		path('index/delete/<pk>', GeoLocDeleteView.as_view(), name='geo-loc-delete_view'),
		path('index/update/<pk>', GeoLocUpdateView.as_view(), name='geo-loc-update_view'),
		# REST
		path('api/v1/', include(('api_v1.urls', 'api_v1'), namespace='apiv1')),
		# JWT
		path('token/obtain/', TokenObtainPairView.as_view(), name='obtain-new-token'),
		path('token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
		path('token/verify/', TokenVerifyView.as_view(), name='verify-token'),
]