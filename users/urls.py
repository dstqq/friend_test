from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('signup/', views.signupPage, name='signup'),
    path('friends/', views.friendsPage, name="friends"),
    path('friend_requests/', views.friend_requests, name="friend_requests"),
    path('cancel_my_friend_request/<int:userID>/', views.cancel_my_friend_request, name='cancel_my_friend_request'),
    path('profile/<str:pk>/', views.userProfile, name='profile'),
    path('update_profile/', views.updadeProfile, name='update_profile'),
    path('send_friend_request/<int:userID>', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:requestID>', views.accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request/<int:requestID>', views.reject_friend_request, name='reject_friend_request'),
    path('delete_from_friends/<int:userID>/', views.delete_from_friends, name='delete_from_friends'),
]
