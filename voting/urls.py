from django.urls import path
from . import views


urlpatterns = [
          path('', views.home, name='home'),
          path('register/', views.register, name='register'),
          path('login/', views.login_view, name='login'),
          path('dashboard/', views.dashboard, name='dashboard'),
          path('add-voter/', views.add_voter, name='add_voter'),
          path('vote/<int:voter_id>/', views.vote, name='vote'),
          path('edit-voter/<int:id>/', views.edit_voter, name='edit_voter'),
          path('delete-voter/<int:id>/', views.delete_voter, name='delete_voter'),
          path('vote/<int:id>/', views.vote, name='vote'),

]