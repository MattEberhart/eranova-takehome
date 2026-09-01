import boto3
import os
from models.invoice_document import InvoiceDocumentMetadata, InvoiceStatus
from models.invoice_extraction import InvoiceExtraction
from decimal import Decimal
import json

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