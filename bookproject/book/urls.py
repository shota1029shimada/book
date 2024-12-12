from django.urls import path
from.import views



urlpatterns = [
    path('',views.ListBookView.as_view(),name='list-book'),
    path('<int:pk>/detail',views.DetailBookView.as_view(),name='detail-book'),
    path('create',views.CreateBookView.as_view(),name='create-book'),
    path('<int:pk>/delete',views.DeleteBookView.as_view(),name='delete-book'),
    path('<int:pk>/update',views.UpdateBookView.as_view(),name='update-book'),
]