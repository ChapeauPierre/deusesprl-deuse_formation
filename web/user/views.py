from typing import Any, Optional
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from user.models import User
from topics.models import Topic
from django.core.paginator import Paginator
from user import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


User = get_user_model()

# Create your views here.


def Register(request):
    if request.method == 'GET':


        return render(request, 'user/register.html')
    
    if request.method == 'POST':

        email =  request.POST.get('email')
        password = request.POST.get('pwd')
        password2 = request.POST.get('pwd_confirm')

        if not email or not password or not password2:
            return render(request, 'user/register.html', {'error': 'Please fill in all fields'})

        if password != password2:
            return render(request, 'user/register.html', {'error': 'Passwords do not match'})
        
        try:
            user = User.objects.get(email=email)
            return render(request, 'user/register.html', {'error': 'User already exists'})
        except User.DoesNotExist:
            user = User.objects.create_user(email, password)
            user.save()
            # end the session with current user if there is one
            if request.user.is_authenticated:
                request.session.flush()
            # log in the new user
            return HttpResponseRedirect(reverse('main:home'))
        
 
class Register(generic.CreateView):

    form_class = forms.CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'user/register.html'

        
# def Profile(request, user_pk):
#     if request.method == 'GET':
#         id = user_pk
#         email = User.objects.get(id=id).email
#         topics = User.objects.get(email=email).topics.all()
#         paginator = Paginator(topics, 3)
#         page_number = request.GET.get('page')
#         page_obj = paginator.get_page(page_number)

#         try:
#             user = User.objects.get(email=email)
#             return render(request, 'user/profile.html', {'user': user, 'page_obj': page_obj}) # TODO nomer differement les variables user obj=user
#         except User.DoesNotExist:
#             return render(request, 'user/profile.html', {'error': 'User does not exist', 'page_obj': page_obj})
        

class Profile(generic.ListView): # list of user's topics

    model = Topic
    template_name = 'user/profile.html'
    context_object_name = 'topics'
    paginate_by = 3

    def get_queryset(self):
        user_pk = self.kwargs['user_pk']
        return Topic.objects.filter(user__id=user_pk)
    
    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        user_pk = self.kwargs['user_pk']
        context['user'] = User.objects.get(id=user_pk)
        return context
    

        
        

def ProfileEdit(request, user_pk):
    id = user_pk
    email = User.objects.get(id=id).email
    if request.method == 'GET':
        if request.user.is_authenticated:
            
            if request.user.email == email:
                return render(request, 'user/profile_edit.html')
            else:
                return HttpResponseRedirect(reverse('user:profile', args=(user_pk,)))
        else:
            return render(request, 'user/profile.html', {'error': 'You must be logged in to edit your profile'})
    if request.method == 'POST': 
        if request.user.is_authenticated:
            if request.user.email == email:
                if request.POST.get('name'):
                    request.user.first_name = request.POST.get('name')
                if request.POST.get('surname'):
                    request.user.last_name = request.POST.get('surname')
                password = request.POST.get('pwd')
                password2 = request.POST.get('pwd_confirmation')

                if password != password2:
                    return render(request, 'user/profile_edit.html', {'error': 'Passwords do not match'})
                
                try:
                    request.user.avatar = request.FILES.get('avatar')
                    
                except:
                    pass

                if password and password2:
                    request.user.set_password(password)
                    
                request.user.save()
                return HttpResponseRedirect(reverse('main:home'))
            else:
                return render(request, 'user/profile.html', {'error': 'You do not have permission to edit this profile'})
        else:
            return render(request, 'user/profile.html', {'error': 'You must be logged in to edit your profile'})

class ProfileEdit(UserPassesTestMixin,generic.UpdateView):
    model = User
    form_class = forms.CustomUserChangeForm
    template_name = 'user/profile_edit.html'

    
    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(ProfileEdit, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
    
    def get_success_url(self):
        return reverse('user:profile', args=(self.request.user.id,))

    # def form_valid(self, form): # TODO: change to django form for change password
    #     if form.cleaned_data['password1'] and form.cleaned_data['password2']:  
    #         if form.cleaned_data['password1'] == form.cleaned_data['password2']:
    #             self.object.set_password(form.cleaned_data['password1'])
    #     return super(ProfileEdit, self).form_valid(form)

    def test_func(self):
        return self.request.user.id == self.kwargs['user_pk']