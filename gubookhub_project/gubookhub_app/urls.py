from django.urls import path
from gubookhub_app import views

app_name='gubookhub_app'

#I've commented out URLs which don't have associated views and templates yet to allow the webapp to run without throwing errors 
urlpatterns = [
    path('', views.index, name = 'index'),
    path('about/', views.about, name = 'about'),
	#path('favourites/', views.favourites, name='favourites'),
	path('search/', views.search, name='search'),
	path('course/<slug:course_name_slug>/add_book/', views.add_book, name='add_book'),
	path('course/<slug:course_name_slug>/', views.show_course, name='show_course'),
	path('subject/<slug:subject_name_slug>/', views.show_subject, name='show_subject'),
	#path('<slug:subject_name_slug>/', views.subjects, name='subjects'),
	#path('<slug:subject_name_slug>/<slug:course_name_slug>/', views.courses, name='courses'),
	#path('<slug:subject_name_slug>/<slug:course_name_slug>/<slug:book_name_slug>/', views.books, name='books'),

]

