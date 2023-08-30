from django.urls import path
from cms import api


urlpatterns = [
    path('<str:token>/', api.CmsAPIView.as_view(), name='cms_edit')
]
