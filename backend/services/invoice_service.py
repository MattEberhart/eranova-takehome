import boto3
import os
import uuid
from models.invoice_document import InvoiceDocumentMetadata, InvoiceStatus, InvoicePage
from datetime import datetime, timezone
from helpers.pagination_helpers import encode_cursor, decode_cursor

class InvoiceService:
    def __init__(self):
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table(os.environ["INVOICE_METADATA_TABLE"])

        self.s3 = boto3.client("s3")
        self.bucket = os.environ["INVOICES_BUCKET"]

        self.extraction_table = self.dynamodb.Table(os.environ["INVOICE_EXTRACTIONS_TABLE"])

    def create_invoice(
        self,
        filename: str,
        content_type
        ) -> InvoiceDocumentMetadata:

        invoice_id = f"inv_{uuid.uuid4()}"
        s3_key = f"invoices/{invoice_id}/{filename}"

        invoice_metadata = InvoiceDocumentMetadata(
            invoice_id=invoice_id,
            s3_key=s3_key,
            filename=filename,
            content_type=content_type,
            status=InvoiceStatus.PENDING_UPLOAD,
            uploaded_at=None,
            created_at=datetime.now,
            record_type="INVOICE"
        )

        self.table.put_item(
            Item=invoice_metadata.model_dump(mode="json")
        )

        return invoice_metadata
        

    def get_invoice(
        self,
        invoice_id:str) -> InvoiceDocumentMetadata | None:
        response = self.table.get_item(
            Key={"invoice_id": invoice_id}
        )

        item = response.get("Item")

        if item is None:
            return None

        return InvoiceDocumentMetadata.model_validate(item)


    def list_invoices(
        self,
        limit: int = 10,
        cursor: str | None = None,
        descending: bool = True) -> list[InvoiceDocumentMetadata]:

        query_args = {
            "IndexName": "invoices-created-at-index",
            "KeyConditionExpression": Key("record_type").eq("INVOICE"),
            "Limit": limit,
            "ScanIndexForward": not descending
        }

        start_key = decode_cursor(cursor)
        if start_key:
            query_args["ExclusiveStartKey"] = exclusive_start_key


        response = self.table.query(**query_args)

        return InvoicePage(
            invoices=[InvoiceDocumentMetadata.model_validate(item) for item in response.get("Items")],
            next_cursor=response.get("LastEvaluatedKey")
        )

    def create_invoice_upload_url(
        self,
        invoice: InvoiceDocumentMetadata) -> str:
        return self.s3.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": self.bucket,
                "Key": invoice.s3_key,
                "ContentType": invoice.content_type
            },
            ExpiresIn=900,
        )

    def get_invoice_url(
        self,
        invoice_document_key: str,
        expires_in: int = 300):

        return self.s3.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": self.bucket,
                "Key": invoice_document_key
            },
            ExpiresIn=expires_in
        )

    def mark_invoice_processing(
            self,
            invoice_id: str,
            status: InvoiceStatus
    ) -> InvoiceDocumentMetadata:
        response = self.table.update_item(
            Key={
                "invoice_id": invoice_id
            },
            UpdateExpression="SET #status = :status, uploaded_at = :uploaded_at",
            ExpressionAttributeNames={
                "#status": "status" # status is a reserved DynamoDb word which is why we need this
            },
            ExpressionAttributeValues={
                ":status": status.value,
                ":uploaded_at": datetime.now(timezone.utc).isoformat()
            },
            ReturnValues="ALL_NEW"
        )

        return InvoiceDocumentMetadata(**response["Attributes"])
        
