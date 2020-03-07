from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
from . import models

def book_list(request):
    books = models.Book.objects.all()
    return render(request, 'book_app/book_list.html', {'books': books})


class BookListView(TemplateView):
    template_name = "book_list.html"

    def get(self, request, *args, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)

        book_objs = models.Book.objects.all()
        context['books'] = book_objs

        return render(self.request, self.template_name, context)