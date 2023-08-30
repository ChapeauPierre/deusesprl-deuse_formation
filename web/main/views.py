from django.views.generic import TemplateView


class HomeTemplateView(TemplateView):
    template_name = 'main/home.html'


class LoginTemplateView(TemplateView):
    template_name = 'main/login.html'


class RegisterTemplateView(TemplateView):
    template_name = 'main/register.html'


class ProfileTemplateView(TemplateView):
    template_name = 'main/profile.html'


class ProfileEditTemplateView(TemplateView):
    template_name = 'main/profile_edit.html'


class TopicListTemplateView(TemplateView):
    template_name = 'main/topic_list.html'


class TopicDetailTemplateView(TemplateView):
    template_name = 'main/topic_detail.html'


class TopicCreateTempalteView(TemplateView):
    template_name = 'main/topic_create.html'


class ReactTempalteView(TemplateView):
    template_name = 'main/react.html'
