import mimetypes
import shutil
import subprocess
from pathlib import Path

import magic


ALLOWED_MIME_TYPES = {
    "application/pdf": {"pdf_to_latex", "pdf_to_word"},
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": {
        "word_to_latex",
        "word_to_pdf",
    },
    "application/x-tex": {"latex_to_pdf", "latex_to_word"},
    "text/x-tex": {"latex_to_pdf", "latex_to_word"},
    "text/plain": {"latex_to_pdf", "latex_to_word"},
}

CONVERSION_OUTPUT_EXT = {
    "pdf_to_latex": ".tex",
    "word_to_latex": ".tex",
    "latex_to_pdf": ".pdf",
    "latex_to_word": ".docx",
    "pdf_to_word": ".docx",
    "word_to_pdf": ".pdf",
}


def detect_mime_type(path: Path) -> str:
    mime = magic.Magic(mime=True)
    return mime.from_file(str(path))


def validate_conversion(path: Path, conversion_type: str) -> None:
    mime_type = detect_mime_type(path)
    if mime_type not in ALLOWED_MIME_TYPES:
        raise ValueError("Unsupported file type")
    if conversion_type not in ALLOWED_MIME_TYPES[mime_type]:
        raise ValueError("Conversion type not allowed for this file type")


def run_command(command: list[str], timeout: int = 240) -> None:
    subprocess.run(command, check=True, timeout=timeout)


def ensure_pandoc_available() -> None:
    if not shutil.which("pandoc"):
        raise RuntimeError("Pandoc is required for conversions")


def ensure_pdflatex_available() -> None:
    if not shutil.which("pdflatex"):
        raise RuntimeError("pdflatex is required for LaTeX conversions")


def ensure_libreoffice_available() -> None:
    if not shutil.which("libreoffice"):
        raise RuntimeError("LibreOffice is required for Word/PDF conversions")


def ensure_pdftotext_available() -> None:
    if not shutil.which("pdftotext"):
        raise RuntimeError("pdftotext is required for PDF conversions")


def convert_pdf_to_latex(input_path: Path, output_path: Path) -> None:
    ensure_pdftotext_available()
    ensure_pandoc_available()
    text_output = output_path.with_suffix(".txt")
    run_command(["pdftotext", str(input_path), str(text_output)])
    run_command([
        "pandoc",
        str(text_output),
        "-f",
        "plain",
        "-t",
        "latex",
        "-o",
        str(output_path),
    ])


def convert_word_to_latex(input_path: Path, output_path: Path) -> None:
    ensure_pandoc_available()
    run_command([
        "pandoc",
        str(input_path),
        "-f",
        "docx",
        "-t",
        "latex",
        "-o",
        str(output_path),
    ])


def convert_latex_to_pdf(input_path: Path, output_path: Path, work_dir: Path) -> None:
    ensure_pdflatex_available()
    run_command([
        "pdflatex",
        "-interaction=nonstopmode",
        f"-output-directory={work_dir}",
        str(input_path),
    ])
    generated_pdf = work_dir / f"{input_path.stem}.pdf"
    generated_pdf.replace(output_path)


def convert_latex_to_word(input_path: Path, output_path: Path) -> None:
    ensure_pandoc_available()
    run_command([
        "pandoc",
        str(input_path),
        "-f",
        "latex",
        "-t",
        "docx",
        "-o",
        str(output_path),
    ])


def convert_pdf_to_word(input_path: Path, output_path: Path) -> None:
    ensure_libreoffice_available()
    run_command([
        "libreoffice",
        "--headless",
        "--convert-to",
        "docx",
        "--outdir",
        str(output_path.parent),
        str(input_path),
    ])
    generated = output_path.parent / f"{input_path.stem}.docx"
    generated.replace(output_path)


def convert_word_to_pdf(input_path: Path, output_path: Path) -> None:
    ensure_libreoffice_available()
    run_command([
        "libreoffice",
        "--headless",
        "--convert-to",
        "pdf",
        "--outdir",
        str(output_path.parent),
        str(input_path),
    ])
    generated = output_path.parent / f"{input_path.stem}.pdf"
    generated.replace(output_path)


def perform_conversion(conversion_type: str, input_path: Path, output_path: Path, work_dir: Path) -> None:
    if conversion_type == "pdf_to_latex":
        convert_pdf_to_latex(input_path, output_path)
    elif conversion_type == "word_to_latex":
        convert_word_to_latex(input_path, output_path)
    elif conversion_type == "latex_to_pdf":
        convert_latex_to_pdf(input_path, output_path, work_dir)
    elif conversion_type == "latex_to_word":
        convert_latex_to_word(input_path, output_path)
    elif conversion_type == "pdf_to_word":
        convert_pdf_to_word(input_path, output_path)
    elif conversion_type == "word_to_pdf":
        convert_word_to_pdf(input_path, output_path)
    else:
        raise ValueError("Unsupported conversion type")


def get_file_extension_for_conversion(conversion_type: str) -> str:
    return CONVERSION_OUTPUT_EXT[conversion_type]


def guess_extension(path: Path) -> str:
    return mimetypes.guess_extension(detect_mime_type(path)) or path.suffix
