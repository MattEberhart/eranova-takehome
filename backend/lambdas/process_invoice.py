from services.invoice_service import InvoiceService
import json

service = InvoiceService()

def handler(event, context):
    return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": "Moved to Processing"
        }