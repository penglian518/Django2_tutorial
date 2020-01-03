from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import get_object_or_404


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

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)  # get the 'num_visits' value, if none assign 0
    request.session['num_visits'] = num_visits + 1

    # The session data will be saved automatically. However, when modified indirectly you have to force it to save
    ## Set session as modified to force data updates/cookie to be saved.
    #request.session.modified = True

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_books_startswithB': num_books_startswithB,
        'num_geners': num_geners,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


from django.views import generic

class BookListView(generic.ListView):
    '''
    By default, the ListView class will use theModelName_list.html as template, e.g. book_list.html. This can be changed
    by setting the 'template_name' variable. e.g template_name = 'books/my_template_name_list.html'.

    the ListView class passes the context as 'book_list' and 'object_list'.

    '''

    model = Book
    paginate_by = 2

    # override the get_queryset() method to change the list of the records returned
    def get_queryset(self):
        return Book.objects.filter(title__startswith='B')[:5]  # Get 5 books containing the title war


class BookDetailView(generic.DetailView):
    '''
    By default, the DetailView class will user theModelName_detail.html, e.g. book_detail.html.

    the DetailView class passes the context as 'book' AND/OR 'object'.
    '''
    model = Book

    def book_detail_view(request, primary_key):
        book = get_object_or_404(Book, pk=primary_key)
        return render(request, 'catalog/book_detail.html', context={'book': book})

class AuthorListView(generic.ListView):

    model = Author
    paginate_by = 2

    # override the get_queryset() method to change the list of the records returned
    def get_queryset(self):
        return Author.objects.filter(last_name__startswith='A')[:5]  # Get 5 authors containing the title war


class AuthorDetailView(generic.DetailView):

    model = Author

    def author_detail_view(request, primary_key):
        author = get_object_or_404(Author, pk=primary_key)
        return render(request, 'catalog/author_detail.html', context={'author': author})

