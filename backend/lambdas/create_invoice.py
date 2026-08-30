from services.invoice_service import InvoiceService
import json
service = InvoiceService()


def handler(event, context):
    body = json.loads(event.get("body") or "{}")

    invoice = service.create_invoice(
        filename=body["filename"],
        content_type=body["contentType"],
    )

    upload_url = service.create_invoice_upload_url(invoice)

    return {
        "statusCode": 201,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "invoice": invoice.model_dump(mode="json"),
            "upload_url": upload_url,
        }),
    }