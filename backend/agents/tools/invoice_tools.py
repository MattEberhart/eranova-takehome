from langchain_core.tools import tool
from services.invoice_service import InvoiceService
from services.invoice_extraction_service import InvoiceExtractionService
from models.invoice_document import InvoiceDocumentMetadata, InvoiceStatus
from models.invoice_extraction import InvoiceExtraction, TaxedLineItem
from uuid import uuid4

invoice_service = InvoiceService()
extraction_service = InvoiceExtractionService()

@tool
def get_invoice_document(invoice_id: str):
    """
    Get a temproary URL for accessing the invoice document.

    Arg: invoice_id. ID of the invoice metadata object.

    Returns: A temporary URL for accessing the invoice document. 
    """
    invoice_metadata: InvoiceDocumentMetadata = invoice_service.get_invoice(invoice_id=invoice_id)
    return invoice_service.get_invoice_url(invoice_metadata.s3_key)


@tool
def put_invoice_extraction(invoice_extraction:InvoiceExtraction) -> InvoiceExtraction:
    """
    Persist the finalized invoice extraction to storage. Also marks the invoice metadata as extracted.
    Arg: Invoice Extraction object to be persisted
    """
    invoice_service.mark_invoice_processing(invoice_extraction.invoice_metadata_id, InvoiceStatus.EXTRACTED)
    return extraction_service.create_invoice_extraction(invoice_extraction=invoice_extraction)

@tool
def convert_to_extraction_result(
    taxed_line_items: list[TaxedLineItem],
    invoice_metadata_id: str):
    """
    Convert the categorized line items and ids to a final InvoiceExtraction object before persisting to storage.
    Arg: categorization result to be converted and the invoice metadata id to be written as well.
    """
    return InvoiceExtraction(
        invoice_extraction_id=str(uuid4()),
        invoice_metadata_id=invoice_metadata_id,
        line_items=taxed_line_items
    )
    