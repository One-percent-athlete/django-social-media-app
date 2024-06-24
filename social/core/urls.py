from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('logout', views.logout, name="logout"),
    path('account_setting', views.account_setting, name="account_setting"),
]