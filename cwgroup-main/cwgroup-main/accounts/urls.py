from django.urls import path

from accounts import views


app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/', views.profile_detail, name='profile'),
    path('profile/update/', views.profile_update, name='profile-update'),
]
