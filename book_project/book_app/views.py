from django.shortcuts import render

from django.views.generic import TemplateView

from book_app.models import Book

class BookListView(TemplateView):
    template_name = "book_list.html"

    def get(self, request, *args, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)

        book_objs = Book.objects.all()
        context['books'] = book_objs

        return render(self.request, self.template_name, context)