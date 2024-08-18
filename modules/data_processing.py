from unstructured.partition.pdf import partition_pdf
from pydantic import BaseModel
from typing import Any, List

class Element(BaseModel):
    type: str
    text: Any

def load_and_partition_pdf(filename: str, path: str = "") -> (List[Element], List[Element]):
    raw_pdf_elements = partition_pdf(
        filename=path + filename,
        extract_images_in_pdf=False,
        infer_table_structure=True,
        chunking_strategy="by_title",
        max_characters=4000,
        new_after_n_chars=3800,
        combine_text_under_n_chars=2000,
    )
    
    categorized_elements = []
    for element in raw_pdf_elements:
        if "unstructured.documents.elements.Table" in str(type(element)):
            categorized_elements.append(Element(type="table", text=str(element)))
        elif "unstructured.documents.elements.CompositeElement" in str(type(element)) or \
             "unstructured.documents.elements.Text" in str(type(element)):
            categorized_elements.append(Element(type="text", text=str(element)))

    table_elements = [e for e in categorized_elements if e.type == "table"]
    text_elements = [e for e in categorized_elements if e.type == "text"]

    return table_elements, text_elements
