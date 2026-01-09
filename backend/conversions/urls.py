from django.urls import path

from .views import ConversionDownloadView, ConversionJobDetailView, ConversionJobListCreateView

urlpatterns = [
    path("jobs/", ConversionJobListCreateView.as_view(), name="conversion-list"),
    path("jobs/<int:pk>/", ConversionJobDetailView.as_view(), name="conversion-detail"),
    path("jobs/<int:pk>/download/", ConversionDownloadView.as_view(), name="conversion-download"),
]
