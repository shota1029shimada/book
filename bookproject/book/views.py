from django.shortcuts import render
from django.urls import reverse_lazy
from.models import Book
from django.views.generic import (
    ListView,DetailView,CreateView,DeleteView,UpdateView,
    )

class ListBookView(ListView):
    template_name='book/book_list.html'
    model=Book

class DetailBookView(DetailView):
    template_name='book/book_detail.html'
    model=Book


class CreateBookView(CreateView):
    template_name='book/book_create.html'
    model=Book
    fields=('title','text','category')#?
    success_url=reverse_lazy('list-book')#django=p159

class DeleteBookView(DeleteView):
    template_name='book/book_confirm_delete.html'
    model=Book
    success_url=reverse_lazy('list-book')#django=p159

class UpdateBookView(UpdateView):
    template_name='book/book_update.html'
    model=Book
    fields=('title','text','category')#? 
    success_url=reverse_lazy('list-book')#django=p159
