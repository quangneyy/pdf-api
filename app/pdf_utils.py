from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import NameObject, ArrayObject

def remove_all_links(input_pdf_path: str, output_pdf_path: str):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    removed_count = 0

    for page in reader.pages:
        if "/Annots" in page:
            annots = []
            for annot in page["/Annots"]: 
                a = annot.get_object()
                subtype = a.get("/Subtype")
                if subtype == "/Link":
                    action = a.get("/A")
                    if action is not None:
                        action_obj = action.get_object() if hasattr(action, "get_object") else action
                        uri = action_obj.get("/URI")
                        if uri:  
                            removed_count += 1
                            print(f"❌ Removed link: {uri}")
                            continue
                annots.append(annot)

            page[NameObject("/Annots")] = ArrayObject(annots)

        writer.add_page(page)

    with open(output_pdf_path, "wb") as f:
        writer.write(f)

    print(f"✅ Total links removed: {removed_count}")