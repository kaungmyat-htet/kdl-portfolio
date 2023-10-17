"""
Api URLs.
"""

from django.conf.urls import include
from django.urls import path

app_name = 'kdl_portfolio'  # pylint: disable=invalid-name
urlpatterns = [
    path('v1/', include('kdl_portfolio.api.v1.urls')),
]
