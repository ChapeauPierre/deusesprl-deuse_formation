import user.serializers

from rest_framework import generics, permissions


class UserCurrentView(generics.RetrieveAPIView):
    """
    An API view allowing authenticated users to read their details.
    """

    serializer_class = user.serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
