from langchain_core.tools import tool
from services.invoice_service import InvoiceService
from services.invoice_extraction_service import InvoiceExtractionService
from models.invoice_document import InvoiceDocumentMetadata, InvoiceStatus
from models.invoice_extraction import InvoiceExtraction, TaxedLineItem
from uuid import uuid4
from pathlib import Path
from agents.constants import INVOICE_AGENT_WORKSPACE_DIR
import shutil
from urllib.request import urlopen

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
def download_invoice_document(invoice_id: str):
    """
    Downloads an invoice document into the file system and returns the local relative path.
    Agent can then use read_file to analyze and extract data from the invoice document.
    Arg: invoice_id
    """
    invoice_metadata: InvoiceDocumentMetadata = invoice_service.get_invoice(invoice_id=invoice_id)

    # Could go to S3 Directly Since It Runs on The Processor Lambda with IAM Access
    # Going with signed url because I have the code to re-use and agent could / should
    # eventually have it's own runtime / environment maybe. download_invoice_document doesn't
    # make much sense elsewhere anyways as far as service code goes.
    invoice_url = invoice_service.get_invoice_url(invoice_metadata.s3_key)

    file_extension = (
        Path(invoice_metadata.s3_key).suffix.lower() or ".pdf"
    )

    relative_path = Path("invoices") / invoice_id / f"invoice{file_extension}"
    full_path = INVOICE_AGENT_WORKSPACE_DIR / relative_path
    full_path.parent.mkdir(parents=True, exist_ok=True)

    with urlopen(invoice_url, timeout=30) as response:
            with full_path.open("wb") as local_file:
                shutil.copyfileobj(response, local_file)

    return f"/{relative_path}"

    

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
    