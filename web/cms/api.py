from rest_framework import generics, status
from rest_framework.response import Response
from cms.models import CustomHTMLContent


class CmsAPIView(generics.UpdateAPIView):
    queryset = CustomHTMLContent.objects.all()
    lookup_field = "token"

    def put(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.data['content'] is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        instance.content = request.data['content']
        instance.save()

        return Response(status=status.HTTP_200_OK)
