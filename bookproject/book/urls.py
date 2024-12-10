from django.urls import path
from.import views

app_name = ''

urlpatterns = [
    path('book/',views.ListBookView.as_view()),
    path('book/<int:pk>/detail',views.DetailBookView.as_view()),
    path('book/create',views.CreateBookView.as_view()),
    path('book/<int:pk>/delete',views.DeleteBookView.as_view(),name='delete-book'),

]