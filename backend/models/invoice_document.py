from datetime import datetime
from pydantic import BaseModel
from enum import Enum

class InvoiceStatus(str, Enum):
    PENDING_UPLOAD = "PENDING_UPLOAD"
    PROCESSING = "PROCESSING"
    EXTRACTED = "EXTRACTED"
    FAILED = "FAILED"

class InvoiceDocumentMetadata(BaseModel):
    invoice_id: str
    s3_key: str
    filename: str
    content_type: str
    status: InvoiceStatus
    uploaded_at: datetime | None
    created_at: datetime | None
    record_type: str

class InvoicePage(BaseModel):
    invoices:list[InvoiceDocumentMetadata]
    next_cursor: str | None
