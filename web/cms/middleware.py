from django.http import HttpResponseRedirect
from django.middleware import csrf


class CmsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.cms_edit = False

    def __call__(self, request):
        if request.GET.get('edit') is not None:
            if request.user.is_superuser:  # TODO use edit permission
                self.cms_edit = True
            else:
                # TODO: redirect to login page
                self.cms_edit = False
        else:
            self.cms_edit = False

        response = self.get_response(request)

        return response

    def process_template_response(self, request, response):
        if response.context_data is not None:
            response.context_data['cms_edit'] = self.cms_edit

            if self.cms_edit:
                response.context_data['cms_csrf_token'] = csrf.get_token(request)

        return response
