import boto3
import os
from models.invoice_document import InvoiceDocumentMetadata, InvoiceStatus
from models.invoice_extraction import InvoiceExtraction
from decimal import Decimal
import json
from boto3.dynamodb.conditions import Key

class InvoiceExtractionService:
    def __init__(self):
        self.dynamodb = boto3.resource("dynamodb")
        self.extraction_table = self.dynamodb.Table(os.environ["INVOICE_EXTRACTIONS_TABLE"])


    def create_invoice_extraction(
        self,
        invoice_extraction:InvoiceExtraction) -> InvoiceExtraction:
        item = json.loads(invoice_extraction.model_dump_json(), parse_float=Decimal)
        self.extraction_table.put_item(Item=item)
        return invoice_extraction

    def get_invoice_extraction_by_metadata_key(
            self,
            invoice_metadata_id: str
    ):
        response = self.extraction_table.query(
            IndexName="invoice-metadata-id-index",
            KeyConditionExpression=Key("invoice_metadata_id")
            .eq(invoice_metadata_id),
            Limit=1,
        )

        items = response.get("Items", [])

        if items is None:
            return None

        return InvoiceExtraction.model_validate(items[0])