from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import tempfile, shutil
from app.pdf_utils import remove_all_links

app = FastAPI(title="PDF Link Remover API")

@app.post("/remove-links/")
async def remove_pdf_links(file: UploadFile = File(...)):
    input_pdf_path = tempfile.mktemp(suffix=".pdf")
    output_pdf_path = tempfile.mktemp(suffix=".pdf")

    with open(input_pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    remove_all_links(input_pdf_path, output_pdf_path)

    return FileResponse(output_pdf_path, media_type="application/pdf", filename="processed.pdf")