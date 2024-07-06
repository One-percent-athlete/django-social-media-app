from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('account_setting', views.account_setting, name="account_setting"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('logout', views.logout, name="logout"),
    path('profile/<str:user_name>', views.profile, name="profile"),
    path('create_post', views.create_post, name="create_post"),
    path('like_post/<str:post_id>', views.like_post, name='like_post'),
    path('follow', views.follow, name='follow'),
    path('search', views.search, name='search')
]