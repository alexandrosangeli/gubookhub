from django.urls import path
from gubookhub_app import views

app_name='gubookhub_app'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('about/', views.about, name = 'about'),
	path('register/', views.register, name='register'), 
	path('login/', views.user_login, name='login'),
	path('favourites/', views.favourites, name='favourites'),
	path('search/', views.search, name='search'),
	path('add_book/', views.add_book, name='add_book'),
	path('<slug:subject_name_slug>/', views.subjects, name='subjects'),
	path('<slug:subject_name_slug>/<slug:course_name_slug>/', views.courses, name='courses'),
	path('<slug:subject_name_slug>/<slug:course_name_slug>/<slug:book_name_slug>/', views.books, name='books'),
]