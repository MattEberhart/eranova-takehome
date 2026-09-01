import boto3
import os
import uuid
from models.invoice_document import InvoiceDocumentMetadata, InvoiceStatus
from datetime import datetime, timezone
from models.invoice_extraction import InvoiceExtraction


class InvoiceExtractionService:
    def __init__(self):
        self.extraction_table = self.dynamodb.Table(os.environ["INVOICE_EXTRACTIONS_TABLE"])


    def create_invoice_extraction(
        self,
        invoice_extraction:InvoiceExtraction) -> InvoiceExtraction:
    
        self.extraction_table.put_item(
        Item=invoice_extraction.model_dump(mode="json")
    )