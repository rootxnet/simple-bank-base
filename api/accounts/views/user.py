from rest_framework import viewsets

from ..models import User
from ..serializers.user import UserSerializer


class CurrentUserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user
