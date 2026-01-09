from rest_framework import serializers

from .models import ConversionJob


class ConversionJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversionJob
        fields = (
            "id",
            "conversion_type",
            "status",
            "file_size",
            "input_file",
            "output_file",
            "created_at",
            "error_message",
        )
        read_only_fields = ("status", "output_file", "created_at", "error_message")
