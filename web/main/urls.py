from django.urls import path

import main.views


app_name = 'main'
urlpatterns = [
    path('', main.views.HomeTemplateView.as_view(), name='home'),
    #path('login/', main.views.LoginTemplateView.as_view(), name='login'),
    #path('register/', main.views.RegisterTemplateView.as_view(), name='register'),
    #path('profile/user_pk/', main.views.ProfileTemplateView.as_view(), name='profile'),
    #path('profile/edit/', main.views.ProfileEditTemplateView.as_view(), name='profile_edit'),
    #path('topics/', main.views.TopicListTemplateView.as_view(), name='topic_list'),
    #path('topics/topic_pk/', main.views.TopicDetailTemplateView.as_view(), name='topic_detail'),
    #path('topics/new/', main.views.TopicCreateTempalteView.as_view(), name='topic_create'),
    path('react/', main.views.ReactTempalteView.as_view(), name='react'),
]
