from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.views import generic
import topics.forms
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.

from topics.models import Topic, Response

def test(request):
    return HttpResponse('test')

# def TopicList(request, query=None): 
#     status = request.GET.get('status', 'all')
#     if status == 'all':
#         topics = Topic.objects.all()
#         status = 'Tous'
#     elif status == 'open':
#         topics = Topic.objects.filter(status='open')
#         status = 'Ouverts'
#     elif status == 'closed':
#         topics = Topic.objects.filter(status='closed')
#         status = 'Fermés'
#     elif status == 'no_responses':
#         topics = Topic.objects.filter(responses__isnull=True)
#         status = 'pas de réponses'
#     else:
#         topics = Topic.objects.all()

#     search_q = request.GET.get('query')

#     if search_q:
#         topics = topics.filter(name__icontains=search_q)
#     else:
#         search_q = ""

#     paginator = Paginator(topics, 3)

#     try:
#         page_number = request.GET['page']
#     except: 
#         page_number = 1

#     page_obj = paginator.get_page(page_number)

#     return render(request, 'topics/topic_list.html', {'topics': topics, 'page_obj': page_obj, 'status': status, 'search_q': search_q})
class TopicList(generic.ListView):
    model = Topic

    template_name = 'topics/topic_list.html'

    context_object_name = 'topics'

    paginate_by = 3

    def get_queryset(self):
        status = self.request.GET.get('status', 'all')
        if status == 'all':
            topics = Topic.objects.all()
            status = 'Tous'
        elif status == 'open':
            topics = Topic.objects.filter(status='open')
            status = 'Ouverts'
        elif status == 'closed':
            topics = Topic.objects.filter(status='closed')
            status = 'Fermés'
        elif status == 'no_responses':
            topics = Topic.objects.filter(responses__isnull=True)
            status = 'pas de réponses'
        else:
            topics = Topic.objects.all()

        search_q = self.request.GET.get('query')

        if search_q:
            topics = topics.filter(name__icontains=search_q)


        return topics

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = self.request.GET.get('status', 'all')
        if self.request.GET.get('query'):
            context['search_q'] = self.request.GET.get('query')
        else:
            context['search_q'] = ""
        return context
    
    
# def TopicDetail(request, topic_pk):
#     if request.method == 'GET':
#         page_number = request.GET.get('page')
#         paginator = Paginator(Response.objects.filter(topic__name=topic_pk), 3)
#         page_obj = paginator.get_page(page_number)
#         if Topic.objects.filter(name=topic_pk).exists():
#             topic = Topic.objects.get(name=topic_pk)
#             return render(request, 'topics/topic_detail.html', {'topic': topic , 'page_obj': page_obj})
#         else:
#             return render(request, 'topics/topic_detail.html', {'error': 'Topic does not exist'})
#     elif request.method == 'POST':
#         text = request.POST.get('message')
#         user = request.user
#         topic = Topic.objects.get(name=topic_pk)
#         response = Response(text=text, user=user, topic=topic)
#         response.save()
#         return HttpResponseRedirect('/topics/details/' + topic.name)

class TopicDetail(generic.ListView):
    model = Response
    

    template_name = 'topics/topic_detail.html'

    context_object_name = 'responses'

    paginate_by = 3

    def get_queryset(self):

        slug = self.kwargs['slug']
        return Response.objects.filter(topic__slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        context['topic'] = Topic.objects.get(slug=slug)
        return context
    
    @method_decorator(login_required)
    def post(self, request, slug):
        text = request.POST.get('message')
        user = request.user
        topic = Topic.objects.get(slug=slug)
        response = Response(text=text, user=user, topic=topic)
        response.save()
        # redirect to last page of topic detail
        return HttpResponseRedirect('/topics/details/' + topic.slug + '?page=' + self.request.GET.get('page', 'last'))
    def get(self, request, slug):
        if not Topic.objects.filter(slug=slug).exists(): # TODO : optimisation directly slug_histoy
            if Topic.objects.filter(slug_history__slug_history=slug).exists():
                topic = Topic.objects.get(slug_history__slug_history=slug)
                return HttpResponseRedirect('/topics/details/' + topic.slug)
            else:
                return HttpResponseRedirect('/topics/details/' + slug)
        else:
            return super().get(request, slug)

# def TopicCreate(request):
#     if request.method == 'GET':
#         if request.user.is_authenticated:
#             return render(request, 'topics/topic_create.html')
#         else:
#             return HttpResponseRedirect('/login')
#     elif request.method == 'POST':
#         name =  request.POST['title']
#         description = request.POST['message']
#         user = request.user
#         topic = Topic(name=name, description=description, user=user)
#         topic.save()
#         return HttpResponseRedirect('/topics/details/' + name)
    
class TopicCreate(generic.CreateView):
    model = Topic

    form_class = topics.forms.TopicCreateForm

    template_name = 'topics/topic_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return '/topics/details/' + self.object.slug

    
# def TopicClose(request, topic_pk):
#     if request.method == 'GET':
#         if request.user.is_authenticated:
#             if Topic.objects.filter(name=topic_pk).exists():
#                 topic = Topic.objects.get(name=topic_pk)
#                 if topic.user == request.user:
#                     topic.status = 'closed'
#                     topic.save()
#                     return HttpResponseRedirect('/topics/details/' + topic.slug)
                
class TopicClose(generic.View):
    def get(self, request, slug):
        if not Topic.objects.filter(slug=slug).exists():
            if Topic.objects.filter(slug_history__slug_history=slug).exists():
                topic = Topic.objects.get(slug_history__slug_history=slug)
                topic.status = 'closed'
                topic.save()
                HttpResponseRedirect('/topics/details/' + topic.slug +'/close')
        if request.user.is_authenticated:
            if Topic.objects.filter(slug=slug).exists():
                topic = Topic.objects.get(slug=slug)
                if topic.user == request.user:
                    topic.status = 'closed'
                    topic.save()
                    return HttpResponseRedirect('/topics/details/' + topic.slug)
                else:
                    return HttpResponseRedirect('/topics/details/' + topic.slug)
            else:
                return HttpResponseRedirect('/topics/details/' + topic.slug)
        else:
            return HttpResponseRedirect('/topics/details/' + topic.slug)
        
    

# def TopicReopen(request, topic_pk):
#     if request.method == 'GET':
#         if request.user.is_authenticated:
#             if Topic.objects.filter(name=topic_pk).exists():
#                 topic = Topic.objects.get(name=topic_pk)
#                 if topic.user == request.user:
#                     topic.status = 'open'
#                     topic.save()
#                     return HttpResponseRedirect('/topics/details/' + topic.slug)

class TopicReopen(generic.View):
    def get(self, request, slug):
        if not Topic.objects.filter(slug=slug).exists():
            if Topic.objects.filter(slug_history__slug_history=slug).exists():
                topic = Topic.objects.get(slug_history__slug_history=slug)
                topic.status = 'open'
                topic.save()
                HttpResponseRedirect('/topics/details/' + topic.slug +'/reopen')
        if request.user.is_authenticated:
            if Topic.objects.filter(slug=slug).exists():
                topic = Topic.objects.get(slug=slug)
                if topic.user == request.user:
                    topic.status = 'open'
                    topic.save()
                    return HttpResponseRedirect('/topics/details/' + topic.slug)
                else:
                    return HttpResponseRedirect('/topics/details/' + topic.slug)
            else:
                return HttpResponseRedirect('/topics/details/' + topic.slug)      
        else:
            return HttpResponseRedirect('/topics/details/' + topic.slug)
                