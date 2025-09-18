from __future__ import annotations

import io
import re
from typing import List

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)
from PyPDF2 import PdfReader
from docx import Document


app = Flask(__name__)
app.secret_key = "change-me"


def extract_text_segments(file_stream: io.BytesIO) -> List[str]:
    """Extract cleaned text segments from the uploaded PDF."""
    reader = PdfReader(file_stream)
    segments: List[str] = []

    for page in reader.pages:
        raw_text = page.extract_text() or ""
        if not raw_text:
            continue

        normalized = raw_text.replace("\r", "\n")
        lines = [line.strip() for line in normalized.split("\n")]
        cleaned_lines = []

        for line in lines:
            if not line:
                cleaned_lines.append("")
                continue

            if re.match(r"^(page|p)\s*\d+\b", line, re.IGNORECASE):
                continue
            if re.match(r"^\d+$", line):
                continue

            cleaned_lines.append(line)

        joined = "\n".join(cleaned_lines)
        for block in re.split(r"\n{2,}", joined):
            block = block.strip()
            if block:
                segments.append(block)

    return segments


@app.route("/", methods=["GET"])
def index():
    return render_template("upload.html")


@app.route("/extract", methods=["POST"])
def extract():
    uploaded = request.files.get("pdf")
    if not uploaded or uploaded.filename == "":
        flash("Please choose a PDF file to upload.")
        return redirect(url_for("index"))

    if not uploaded.filename.lower().endswith(".pdf"):
        flash("Only PDF files are supported.")
        return redirect(url_for("index"))

    file_bytes = io.BytesIO(uploaded.read())
    file_bytes.seek(0)

    try:
        segments = extract_text_segments(file_bytes)
    except Exception:  # pragma: no cover - PyPDF2 errors bubble up rarely
        flash("We couldn't read that PDF. Please try a different file.")
        return redirect(url_for("index"))

    if not segments:
        flash("No readable text was found in the PDF.")
        return redirect(url_for("index"))

    session["segments"] = segments
    return render_template("review.html", segments=segments)


@app.route("/download", methods=["POST"])
def download():
    stored_segments = session.get("segments")
    if not stored_segments:
        flash("Please upload a PDF before requesting a download.")
        return redirect(url_for("index"))

    selected_indices = request.form.getlist("segment")
    if not selected_indices:
        flash("Select at least one section to keep.")
        return render_template("review.html", segments=stored_segments)

    chosen_segments = [stored_segments[int(index)] for index in selected_indices]

    document = Document()
    document.add_heading("Recipe", level=1)
    for segment in chosen_segments:
        document.add_paragraph(segment)

    output = io.BytesIO()
    document.save(output)
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="recipe.docx",
        mimetype=(
            "application/vnd.openxmlformats-officedocument."
            "wordprocessingml.document"
        ),
    )


if __name__ == "__main__":
    app.run(debug=True)
