from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index')
]

# The 'name' parameter is a unique identifier for this URL mapping, which can be called from the template.
# e.g. <a href="{% url 'index' %}">Home</a>.
# If hard coded to <a href="/catalog/">Home</a>, we'll have to change the template when the URL mapping changed.
#

