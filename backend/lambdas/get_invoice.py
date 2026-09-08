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
    if invoice_metadata.status is InvoiceStatus.PENDING_UPLOAD:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invoice not uploadeed."})
        }

    invoice_document_url:str = invoice_metadata_service.get_invoice_url(invoice_metadata.s3_key)

    # Not sure about this behavior, should maybe still succeed if extraction in progress
    # Just putting this for now
    if invoice_metadata.status is not InvoiceStatus.EXTRACTED:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invoice not yet extracted"})
        }
    invoice_extraction:InvoiceExtraction = extraction_service.get_invoice_extraction_by_metadata_key(invoice_id)
    
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "invoice_metada": invoice_metadata.model_dump_json(),
            "invoice_document_url": invoice_document_url,
            "invoice_extraction": invoice_extraction.model_dump_json
        })
    }