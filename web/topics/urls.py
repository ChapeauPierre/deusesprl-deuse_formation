from django.urls import path

import topics.views


app_name = 'topics'
urlpatterns = [
    #path('topics/', topics.views.TopicList, name='topic_list'),
    path('topics/', topics.views.TopicList.as_view(), name='topic_list'),
    #path('topics/details/<str:topic_pk>/', topics.views.TopicDetail, name='topic_detail'),
    
    path('topics/details/<str:slug>/', topics.views.TopicDetail.as_view(), name='topic_detail'),

    #path('topics/details/<str:slug>/close/', topics.views.TopicClose, name='topic_close'),
    path('topics/details/<str:slug>/close/', topics.views.TopicClose.as_view(), name='topic_close'),

    #path('topics/details/<str:slug>/reopen/', topics.views.TopicReopen, name='topic_reopen'),
    path('topics/details/<str:slug>/reopen/', topics.views.TopicReopen.as_view(), name='topic_reopen'),

    #path('new/topics/', topics.views.TopicCreate, name='topic_create'),
    path('new/topics/', topics.views.TopicCreate.as_view(), name='topic_create'),

]
