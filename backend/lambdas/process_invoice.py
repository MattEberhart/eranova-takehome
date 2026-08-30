from services.invoice_service import InvoiceService
from models.invoice import InvoiceStatus
import json

service = InvoiceService()

def handler(event, context):

    s3_event = event["Records"][0]
    s3_key = s3_event["s3"]["object"]["key"]

    # Parse out invoice id as defined in invoice_service create_invoice
    s3_key_pieces = s3_key.split("/")
    invoice_id = s3_key_pieces[1]

    service.update_invoice_status(invoice_id=invoice_id, status=InvoiceStatus)

    return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": "Moved to Processing"
        }