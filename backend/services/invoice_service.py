import boto3
import os
import uuid
from models.invoice import InvoiceMetadata, InvoiceStatus
from datetime import datetime, timezone

class InvoiceService:
    def __init__(self):
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table(os.environ["INVOICE_METADATA_TABLE"])

        self.s3 = boto3.client("s3")
        self.bucket = os.environ["INVOICES_BUCKET"]

    def create_invoice(
        self,
        filename: str,
        content_type
        ) -> InvoiceMetadata:

        invoice_id = f"inv_{uuid.uuid4()}"
        s3_key = f"invoices/{invoice_id}/{filename}"

        invoice_metadata = InvoiceMetadata(
            invoice_id=invoice_id,
            s3_key=s3_key,
            content_type=content_type,
            status=InvoiceStatus.PENDING_UPLOAD,
            uploaded_at=None
        )

        self.table.put_item(
            Item=invoice_metadata.model_dump(mode="json")
        )

        return invoice_metadata

    def get_invoice(
        self,
        invoice_id:str) -> InvoiceMetadata | None:
        response = self.table.get_item(
            Key={"invoiceId": invoice_id}
        )

        item = response.get("Item")

        if item is None:
            return None

        return InvoiceMetadata.model_validate(item)


    def list_invoices(
        self,
        limit: int = 10) -> list[InvoiceMetadata]:
        response = self.table.scan(Limit=limit)
        return [
            InvoiceMetadata.model_validate(item)
            for item in response.get("Items", [])
        ]

    def create_invoice_upload_url(
        self,
        invoice: InvoiceMetadata) -> str:
        return self.s3.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": self.bucket,
                "Key": invoice.source_s3_key,
                "ContentType": invoice.content_type,
            },
            ExpiresIn=900,
        )

    def mark_invoice_processing(
            self,
            invoice_id: str,
            status: InvoiceStatus
    ) -> InvoiceMetadata:
        response = self.table.update_item(
            Key={
                "invoice_id": invoice_id
            },
            UpdateExpression="SET #status = :status, uploaded_at = :uploaded_at",
            ExpressionAttributeNames={
                "status": "status"
            },
            ExpressionAttributeValues={
                ":status": InvoiceStatus.PROCESSING.value,
                ":uploaded_at": datetime.now(timezone.utc).isoformat()
            },
            ReturnValues="ALL_NEW"
        )

        return InvoiceMetadata(**response["Attributes"])
        
