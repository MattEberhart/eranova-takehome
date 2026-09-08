from services.invoice_service import InvoiceService
import json
from models.invoice_document import InvoicePage

service = InvoiceService()


def handler(event, context):

    params = event.get("queryStringParameters") or {}
    limit = params.get("limit", 20)
    order = params.get("order", "desc").lower()
    cursor = params.get("cursor")
    descending = order == "desc"

    invoice_page = service.list_invoices(
        limit=limit,
        cursor=cursor,
        descending=descending
    )

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": invoice_page.model_dump_json()
    }