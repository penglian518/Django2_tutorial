from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

import datetime
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import RenewBookForm


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

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    # to restrict our query to just the BookInstance objects for the current user
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class AllLoanedBooksListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan."""
    permission_required = ('catalog.can_mark_returned',)

    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    # to restrict our query to just the BookInstance objects for the current user
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    '''view func for renewing a book instance'''
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # if this is a POST request, then process the Form data
    if request.method == 'POST':

        # Binding. Create a form instance and populate it with data from the request
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # if this is a GET (or other method) create the default form
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


# generic editing views
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalog.models import Author

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')


from catalog.models import Book

class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    #initial = {'date_of_death': '05/01/2018'}

class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')

