from services.invoice_service import InvoiceService
import json

service = InvoiceService()


def handler(event, context):
    invoice_id = event["pathParameters"]["invoice_id"]

    invoice = service.get_invoice(invoice_id)

    if invoice is None:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Invoice not found"}),
        }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": invoice.model_dump_json(),
    }