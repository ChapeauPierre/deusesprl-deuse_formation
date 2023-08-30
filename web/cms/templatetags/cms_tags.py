import cms.models

from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.middleware import csrf
from django.template import TemplateSyntaxError
from django.utils.safestring import mark_safe


register = template.Library()


# Custom tags
@register.simple_tag(name='cms', takes_context=True)
def cms_tag(context, token, default_content=None):
    """
    Display a custom HTML content.
    Usage::
        {% cms token %}
    This tries to find the equivalent CustomHTMLContent model and display this
    content field.

    There is a second form::
        {% cms token "this is a test" %}
    This tries to find the equivalent CustomHTMLContent model and display this
    content field.
    If An exception occurs, we create new instance and display the contents of
    the string.

    You can use variables instead of constant strings as default_content::
        {% cms token default_variable %}
    This tries to find the equivalent CustomHTMLContent model.
    If An exception occurs, we create new instance and the contents of
    the variable ``default_variable``.
    """

    try:
        instance = cms.models.CustomHTMLContent.objects.get(token=token)
    except ObjectDoesNotExist:
        if default_content is None:
            default_content = " "

        if default_content:
            instance = cms.models.CustomHTMLContent.objects.create(
                token=token,
                content=default_content)
        else:
            raise TemplateSyntaxError(
                "cms tag: Invalid argument '%s' provided." % token)

    if instance.content is not None:
        text = instance.content
    else:
        text = ""

    if context['cms_edit']:
        return mark_safe('<div class="cms_edit" token="' + token + '">' + text + '</div>')
    else:
        return mark_safe(text)


@register.simple_tag(name='cms_image', takes_context=True)
def cms_image(context, token, class_name=None):
    """
    Display a custom image.
    Usage::
        {% cms_image token [class_name] %}
    This tries to find the equivalent CustomImage model and display the image.
    If An exception occurs, we create new instance and display a default image.
    If class_name is provided, the image will have that string as the class parameter.
    """

    try:
        instance = cms.models.CustomImage.objects.get(token=token)
    except ObjectDoesNotExist:
        instance = cms.models.CustomImage.objects.create(
            token=token,
            alt="Undefined image"
        )

    if instance.image:
        src_str = ' src="' + instance.image.url + '"'
        alt = ' alt="' + instance.alt + '"'
    else:
        src_str = ''
        alt = 'image: ' + token

    if class_name is not None:
        class_str = ' class="' + class_name + '"'
    else:
        class_str = ""

    return mark_safe('<img' + class_str + src_str + alt + '"/>')


@register.simple_tag(name='cms_save', takes_context=True)
def cms_save_tag(context, text):
    """
    Insert this tag where you want the save button to be
    """

    if context['cms_edit']:
        return mark_safe('<div id="cms_save" csrf_token="' + context['cms_csrf_token'] + '">' + text + '</div>')
    else:
        return ""
