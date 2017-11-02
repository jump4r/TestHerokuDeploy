from django.conf.urls import url
from catalog.views import AppView


urlpatterns = [
    url(r'^$', AppView.as_view())
]