from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from core.views import index,login_request, logout_request, google_login_callback, Signup, \
    AdminView, view_installs, GetAllInstalls
urlpatterns = [
    #...
    path('', index, name='index'),
    path('login/', login_request, name='login'),
    path('signup/', Signup.as_view(), name='signup'),
    path('admin-page/',AdminView.as_view(), name='admin-page'),
    path('view-installs/', view_installs, name='view-installs'),
    path('get-all-installs/', GetAllInstalls.as_view(), name='get-all-installs'),
    path('google-login-callback/',google_login_callback,name='google-login-callback'),
    
    path('accounts/', include('allauth.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),

]