from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse,reverse_lazy
from.models import Book,Review
from django.views.generic import (
    ListView,DetailView,CreateView,DeleteView,UpdateView,
    )
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout#追加
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from.consts import ITEM_PER_PAGE
from .forms import SearchForm
from django.db.models import Avg, Case, When, Value, IntegerField #def index_view(request):

class ListBookView(LoginRequiredMixin,ListView):
    template_name='book/book_list.html'
    model=Book
    paginate_by=ITEM_PER_PAGE

class DetailBookView(LoginRequiredMixin,DetailView):
    template_name='book/book_detail.html'
    model=Book


class CreateBookView(LoginRequiredMixin,CreateView):
    template_name='book/book_create.html'
    model=Book
    fields=('title','text','category','thumbnail')#?
    success_url=reverse_lazy('list-book')#django=p159

    def form_vaild(self,form):
        form.instance.user=self.request.user

        return super().form_vaild(form)#追加

class DeleteBookView(LoginRequiredMixin,DeleteView):
    template_name='book/book_confirm_delete.html'
    model=Book
    success_url=reverse_lazy('list-book')#django=p159
    def get_object(self,queryset=None):
        obj=super().get_object(queryset)
        if obj.user !=self.request.user:
            raise PermissionDenied
        return obj

class UpdateBookView(LoginRequiredMixin,UpdateView):
    template_name='book/book_update.html'
    model=Book
    fields=('title','text','category','thumbnail')#? 
    #success_url=reverse_lazy('list-book')django=p159

    def get_object(self,queryset=None):
        obj=super().get_object(queryset)
        if obj.user !=self.request.user:
            print(obj.user)
            print(self.request.user)
            raise PermissionDenied
        return obj
    
    def get_success_url(self):
        return reverse('detail-book', kwargs={'pk':self.object.id})
    

def index_view(request):
    queryset = Book.objects.all()

    #検索機能
    searchForm = SearchForm(request.GET)
    if searchForm.is_valid():                       #フォームが有効な場合、
        keyword = searchForm.cleaned_data['keyword']#キーワードを取得し、そのキーワードを含む本のリストを
        queryset=Book.objects.filter(title__contains=keyword)# object_list に格納
    # 平均評価の計算
    queryset = queryset.annotate(avg_rating=Avg('review__rate'))
    
    #ソート機能
    sort_option = request.GET.get('rate', '最新投稿順')
    if sort_option == '最新投稿順':
        queryset = queryset.order_by('-id')
    elif sort_option == '古い投稿順':
        queryset = queryset.order_by('id')
    elif sort_option == '評価':
        queryset = queryset.order_by('-avg_rating', '-id')
    else:
        queryset = queryset.order_by('-id')

  #ページネーション
    paginator = Paginator(queryset, ITEM_PER_PAGE)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.page(page_number)

        
    # テンプレートにはpage_objのみを渡す（ranking_listは不要）
    context = {
        'selected_option': sort_option,
        'searchForm': searchForm,
        'page_obj': page_obj,  # ページネーション済みのオブジェクト
        'object_list': queryset,  # 追加: querysetをcontextに渡す
    }
    return render(
        request, 'book/index.html', context)
        #'book/index.html',
        #{'object_list':object_list, 'ranking_list':ranking_list,'page_obj':page_obj},)

class CreateReviewView(LoginRequiredMixin,CreateView):
    model=Review
    fields=('book','title','text','rate')
    template_name='book/review_form.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['book']=Book.objects.get(pk=self.kwargs['book_id'])
        return context
    
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('detail-book', kwargs={'pk':self.object.book.id})
    