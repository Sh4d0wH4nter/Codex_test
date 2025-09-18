# Recipe PDF Extractor

This project is a small Flask web application that lets you upload a recipe PDF, break it into readable chunks, visually organise the text, and export the curated content to a Word document.

## Features

- Upload any PDF that contains a recipe.
- Automatic cleaning that removes common noise such as empty lines and page numbers.
- Each sentence or bullet is extracted so you can drag it into the recipe category that fits best.
- Create custom categories on the fly, and drop anything irrelevant into the **Discard** column.
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
- Continuous blank lines are collapsed and then split into sentence-sized segments.
- The review page shows a drag-and-drop board where you can assign each segment to categories or discard it.
- When you click **Download Word document**, the app builds a `.docx` file using `python-docx` grouped under the headings you chose.

## Notes

- This extractor focuses on text-based PDFs. Scanned PDFs that require OCR are not supported out of the box.
- The automatic cleaning is intentionally conservative so that you stay in control—use the drag-and-drop step to fine-tune the final output.
