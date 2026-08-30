from services.invoice_service import InvoiceService
import json

service = InvoiceService()


def handler(event, context):
    invoices = service.list_invoices()

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": {
            "invoices": json.dumps([
            invoice.model_dump(mode="json")
            for invoice in invoices
        ]),
        }
    }