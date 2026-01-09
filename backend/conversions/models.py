from django.conf import settings
from django.db import models


class ConversionJob(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    TYPE_CHOICES = [
        ("pdf_to_latex", "PDF to LaTeX"),
        ("word_to_latex", "Word to LaTeX"),
        ("latex_to_pdf", "LaTeX to PDF"),
        ("latex_to_word", "LaTeX to Word"),
        ("pdf_to_word", "PDF to Word"),
        ("word_to_pdf", "Word to PDF"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    input_file = models.FileField(upload_to="inputs/")
    output_file = models.FileField(upload_to="outputs/", null=True, blank=True)
    conversion_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    file_size = models.PositiveBigIntegerField()
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.conversion_type}"
