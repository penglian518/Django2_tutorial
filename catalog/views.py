from django.shortcuts import render
from django.shortcuts import HttpResponse

# Create your views here.

from catalog.models import Book, Author, BookInstance, Genre

def home(request):

    return HttpResponse('this is catalog home')


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Books start with B
    num_books_startswithB = Book.objects.filter(title__startswith='B').count()
    num_geners = Genre.objects.all().count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_books_startswithB': num_books_startswithB,
        'num_geners': num_geners,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
