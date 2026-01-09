import shutil
import tempfile
from pathlib import Path

from celery import shared_task
from django.core.files import File
from django.db import transaction

from .models import ConversionJob
from .utils import get_file_extension_for_conversion, perform_conversion, validate_conversion


@shared_task(bind=True)
def run_conversion(self, job_id: int) -> None:
    job = ConversionJob.objects.get(id=job_id)
    job.status = "processing"
    job.save(update_fields=["status"])

    with tempfile.TemporaryDirectory() as tmp_dir:
        work_dir = Path(tmp_dir)
        input_path = work_dir / job.input_file.name.split("/")[-1]
        with job.input_file.open("rb") as source_file:
            with open(input_path, "wb") as target_file:
                shutil.copyfileobj(source_file, target_file)

        validate_conversion(input_path, job.conversion_type)
        output_extension = get_file_extension_for_conversion(job.conversion_type)
        output_path = work_dir / f"output{output_extension}"

        try:
            perform_conversion(job.conversion_type, input_path, output_path, work_dir)
        except Exception as exc:
            job.status = "failed"
            job.error_message = str(exc)
            job.save(update_fields=["status", "error_message"])
            raise

        with transaction.atomic():
            with open(output_path, "rb") as output_file:
                job.output_file.save(output_path.name, File(output_file), save=False)
            job.status = "completed"
            job.save(update_fields=["output_file", "status"])
