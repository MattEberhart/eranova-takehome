from agents.tools.invoice_tools import download_invoice_document
from models.invoice_extraction import LineItemExtractionResult

LINE_ITEM_EXTRACTOR_SYSTEM_PROMPT = """
You are an invoice line item extraction specialist.

1.Download the invoice to your local file system using download_invoice_document tool. It will return the relative path to the document.

2.Read the invoice document and extract every line item.

3.Each line item consists of the following:
- quantity
- item_price
- description
- total_amount

4.Return a list of line items as specified by the LineItemExtractionResult response_format.
"""

line_item_extractor = {
    "name": "line-item-extractor",
    "description": (
        "Reads an invoice document of any time (PDF, image, structured, unstructured) and extracts all line items."

    ),
    "model":"openai:gpt-5.5", # Maybe fine for pdfs / text based? Need to switch it on the fly later for images?
    "system_prompt": LINE_ITEM_EXTRACTOR_SYSTEM_PROMPT,
    "tools": [ download_invoice_document ], # Will not inherit others
    "response_format": LineItemExtractionResult
}

