from services.invoice_service import InvoiceService
from models.invoice_document import InvoiceStatus
import json
from agents.invoice_processor import invoice_processor
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

service = InvoiceService()

def handler(event, context):

    s3_event = event["Records"][0]
    s3_key = s3_event["s3"]["object"]["key"]

    # Parse out invoice id as defined in invoice_service create_invoice
    s3_key_pieces = s3_key.split("/")
    invoice_id = s3_key_pieces[1]

    service.mark_invoice_processing(invoice_id=invoice_id, status=InvoiceStatus.PROCESSING)

    thread_id = f"invoice:{invoice_id}" # This means we can only process/ have one thread per upload. Maybe not great, something to notes.

    try:
        result = invoice_processor.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": f"Process invoice {invoice_id}"
                    }
                ]
            },
            config={
                "configurable": {
                    "thread_id": thread_id
                }
            }
        )
    except Exception:
        logger.exception("Invoice processing agent failed.")
        service.mark_invoice_processing(
            invoice_id=invoice_id,
            status=InvoiceStatus.FAILED
        )
        # Not re raisng. Wasting tokens / money on retries. Will just return 200 for nwo
        #raise ## re throws. Causes lambda to retry the S3 event.
                ## Not sure we need the retry, so far retries are finding same failure path
                ## Maybe retries good when we get passed code issues and get to agentic decisions

    return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": f"Invoice processed"
        }