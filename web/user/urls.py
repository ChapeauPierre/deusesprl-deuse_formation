from django.urls import include, path
import user.views


app_name = 'user'
urlpatterns = [
    
    #path('register/', user.views.Register, name='register'),
    path('register/', user.views.Register.as_view(), name='register'),
    #path('profile/<int:user_pk>/', user.views.Profile, name='profile'),
    path('profile/<int:user_pk>/', user.views.Profile.as_view(), name='profile' ),
    #path('profile/<int:user_pk>/edit/', user.views.ProfileEdit, name='profile_edit'),
    path('profile/<int:user_pk>/edit/', user.views.ProfileEdit.as_view(), name='profile_edit'),
    
]
