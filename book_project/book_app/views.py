from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
from . import models
from . import forms

def book_list(request):
    books = models.Book.objects.all()
    return render(request, 'book_app/book_list.html', {'books': books})


def book_new(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            # post.author = request.user
            # post.published_date = timezone.now()
            post.save()
    else:
        form = forms.BookForm()
    return render(request, 'book_app/book_new.html', {'form': form})


class BookListView(TemplateView):
    template_name = "book_list.html"

    def get(self, request, *args, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)

        book_objs = models.Book.objects.all()
        context['books'] = book_objs

        return render(self.request, self.template_name, context)