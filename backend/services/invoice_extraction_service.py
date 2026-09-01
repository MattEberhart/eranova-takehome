import boto3
import os
from models.invoice_document import InvoiceDocumentMetadata, InvoiceStatus
from models.invoice_extraction import InvoiceExtraction
from decimal import Decimal

class InvoiceExtractionService:
    def __init__(self):
        self.dynamodb = boto3.resource("dynamodb")
        self.extraction_table = self.dynamodb.Table(os.environ["INVOICE_EXTRACTIONS_TABLE"])


    def create_invoice_extraction(
        self,
        invoice_extraction:InvoiceExtraction) -> InvoiceExtraction:
    
        self.extraction_table.put_item(
        Item=invoice_extraction.model_dump(mode="json", parse_float=Decimal,)
    )