from django.urls import path
from .import views

urlpatterns = [
    path("", views.home, name ="home"), #Specify path that connects a URL pattern to a specific path/view
    path("add/",views.add_book, name ="add"),
    path("edit/",views.edit_book, name ="edit"),
    path("edit/extend_edit<int:book_id>/",views.edit_book, name ="extend"),
    path("delete/", views.delete_book, name="delete_book"),
]