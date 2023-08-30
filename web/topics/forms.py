from django.forms import ModelForm
from topics.models import Topic

class TopicCreateForm(ModelForm):


    class Meta:
        model = Topic
        fields = ['name', 'description']

