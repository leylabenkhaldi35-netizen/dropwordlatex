from rest_framework import generics

from .models import Subscription
from .serializers import SubscriptionSerializer


class SubscriptionDetailView(generics.RetrieveAPIView):
    serializer_class = SubscriptionSerializer

    def get_object(self):
        subscription, _ = Subscription.objects.get_or_create(user=self.request.user)
        return subscription
