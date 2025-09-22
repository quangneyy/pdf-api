import fitz

def remove_all_links_and_text(input_pdf_path: str, output_pdf_path: str, texts_to_remove: list[str] = None):
    doc = fitz.open(input_pdf_path)

    removed_links = 0
    removed_texts = 0

    for page in doc:
        links = page.get_links()
        for l in links:
            uri = l.get("uri", None)
            if uri:
                removed_links += 1
                print(f"❌ Removed link: {uri}")
                page.delete_link(l)

        if texts_to_remove:
            for t in texts_to_remove:
                text_instances = page.search_for(t)
                for inst in text_instances:
                    page.add_redact_annot(inst, fill=(1, 1, 1))
                    removed_texts += 1
                    print(f"❌ Removed text: {t}")

            page.apply_redactions()

    doc.save(output_pdf_path)
    doc.close()

    print(f"✅ Total links removed: {removed_links}")
    print(f"✅ Total texts removed: {removed_texts}")