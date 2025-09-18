# Recipe PDF Extractor

This project is a small Flask web application that lets you upload a recipe PDF, cleanly extract the meaningful text, review the extracted sections, and export the selected content to a Word document.

## Features

- Upload any PDF that contains a recipe.
- Automatic cleaning that removes common noise such as empty lines and page numbers.
- Review interface where you can uncheck any sections you do not want to keep.
- Download the curated recipe in a standard `.docx` (Word) format.

## Requirements

- Python 3.11+
- The dependencies listed in `requirements.txt`

## Getting Started

1. (Optional) Create and activate a virtual environment.
2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   flask --app app run
   ```

4. Open your browser to `http://127.0.0.1:5000/` and upload a recipe PDF.

## How it works

- `PyPDF2` is used to extract the text from the PDF pages.
- Lines that only contain a page number are filtered out.
- Continuous blank lines are collapsed into paragraph-sized sections.
- The review page displays each section with checkboxes so you can choose what to keep.
- When you click **Download Word document**, the app builds a `.docx` file using `python-docx` with each selected section as a paragraph.

## Notes

- This extractor focuses on text-based PDFs. Scanned PDFs that require OCR are not supported out of the box.
- The automatic cleaning is intentionally conservative so that you stay in control—use the review step to fine-tune the final output.
