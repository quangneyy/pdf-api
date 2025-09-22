from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
import tempfile, shutil, json
from app.pdf_utils import remove_all_links_and_text

app = FastAPI(title="PDF Link & Text Remover API")

@app.post("/remove-links-and-text/")
async def remove_pdf_links_and_text(
    file: UploadFile = File(...),
    texts: str = Form(default="[]") 
):
    input_pdf_path = tempfile.mktemp(suffix=".pdf")
    output_pdf_path = tempfile.mktemp(suffix=".pdf")

    with open(input_pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        texts_to_remove = json.loads(texts)
        if not isinstance(texts_to_remove, list):
            texts_to_remove = []
    except Exception:
        texts_to_remove = []

    remove_all_links_and_text(input_pdf_path, output_pdf_path, texts_to_remove)

    return FileResponse(
        output_pdf_path,
        media_type="application/pdf",
        filename="processed.pdf"
    )