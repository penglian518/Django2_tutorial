from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),

    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    #re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),


]

# The 'name' parameter is a unique identifier for this URL mapping, which can be called from the template.
# e.g. <a href="{% url 'index' %}">Home</a>.
# If hard coded to <a href="/catalog/">Home</a>, we'll have to change the template when the URL mapping changed.
#

# The generic class-based detail view expects to be passed a parameter named pk.
# If you're writing your own function view you can use whatever parameter name you like,
# or indeed pass the information in an unnamed argument.
#

# <> define the part of the URL to be captured, enclosing the name of the variable that the view can use to access
# the captured data. E.g. <something> , will capture the marked pattern and pass the value to the view
# as a variable "something".
#

# re_path() uses a Regular expression to map the url




