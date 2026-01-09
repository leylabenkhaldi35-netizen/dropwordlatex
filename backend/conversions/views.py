from datetime import timedelta

from django.http import FileResponse
from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView

from subscriptions.models import Subscription

from .models import ConversionJob
from .serializers import ConversionJobSerializer
from .tasks import run_conversion

FREE_MAX_SIZE = 20 * 1024 * 1024
PREMIUM_MAX_SIZE = 200 * 1024 * 1024
FREE_DAILY_LIMIT = 5


def is_premium(user) -> bool:
    if user.role in {"premium", "admin"}:
        return True
    subscription = Subscription.objects.filter(user=user, active=True, plan="premium").first()
    return subscription is not None


class ConversionJobListCreateView(generics.ListCreateAPIView):
    serializer_class = ConversionJobSerializer
    parser_classes = [MultiPartParser]

    def get_queryset(self):
        return ConversionJob.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        input_file = self.request.data.get("input_file")
        conversion_type = self.request.data.get("conversion_type")
        if not input_file:
            raise ValidationError("input_file is required")
        if not conversion_type:
            raise ValidationError("conversion_type is required")

        file_size = input_file.size
        premium = is_premium(self.request.user)
        max_size = PREMIUM_MAX_SIZE if premium else FREE_MAX_SIZE
        if file_size > max_size:
            raise ValidationError("File size exceeds plan limit")

        if not premium:
            window_start = timezone.now() - timedelta(days=1)
            count = ConversionJob.objects.filter(
                user=self.request.user, created_at__gte=window_start
            ).count()
            if count >= FREE_DAILY_LIMIT:
                raise PermissionDenied("Daily conversion limit reached")

        job = serializer.save(user=self.request.user, file_size=file_size)
        run_conversion.delay(job.id)


class ConversionJobDetailView(generics.RetrieveAPIView):
    serializer_class = ConversionJobSerializer

    def get_queryset(self):
        return ConversionJob.objects.filter(user=self.request.user)


class ConversionDownloadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        job = ConversionJob.objects.filter(user=request.user, pk=pk).first()
        if not job:
            raise PermissionDenied("Not found")
        if job.status != "completed" or not job.output_file:
            raise ValidationError("Conversion not completed")
        response = FileResponse(job.output_file.open("rb"), as_attachment=True)
        response["Content-Disposition"] = f'attachment; filename="{job.output_file.name.split("/")[-1]}"'
        return response
