from services.invoice_service import InvoiceService
import json
from services.invoice_extraction_service import InvoiceExtractionService
from models.invoice_document import InvoiceDocumentMetadata, InvoiceStatus
from models.invoice_extraction import InvoiceExtraction

invoice_metadata_service:InvoiceService = InvoiceService()
extraction_service:InvoiceExtractionService = InvoiceExtractionService()


def handler(event, context):
    invoice_id = event["pathParameters"]["invoice_id"]

    invoice_metadata:InvoiceDocumentMetadata = invoice_metadata_service.get_invoice(invoice_id)

    if invoice_metadata is None:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Invoice not found"}),
        }
    if invoice_metadata.status == InvoiceStatus.PENDING_UPLOAD:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invoice not uploadeed."})
        }

    invoice_document_url:str = invoice_metadata_service.get_invoice_url(invoice_metadata.s3_key)

    invoice_extraction: InvoiceExtraction | None = None
    if invoice_metadata.status == InvoiceStatus.EXTRACTED:
        invoice_extraction = extraction_service.get_invoice_extraction_by_metadata_key(invoice_id)
    
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "invoice_metadata": invoice_metadata.model_dump(mode="json"),
            "invoice_document_url": invoice_document_url,
            "invoice_extraction": invoice_extraction.model_dump(mode="json") if invoice_extraction is not None else None
        })
    }