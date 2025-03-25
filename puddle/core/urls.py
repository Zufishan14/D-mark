from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import LoginForm
from .views import logout

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
    path('logout_user', views.logoutUser, name='logout'),	
    path('sql-data/', views.sql_data, name='sql_data'),
    path('edit-sql/', views.edit_sql, name='edit_sql'),
    path('add-record/', views.add_record, name='add_record'),
    path('edit-record/<int:pk>/', views.edit_record, name='edit_record'),
    path('delete-record/<int:pk>/', views.delete_record, name='delete_record'),
]

from django.urls import path
from django.contrib.auth.views import LogoutView
