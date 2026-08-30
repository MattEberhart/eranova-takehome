from datetime import datetime
from pydantic import BaseModel
from enum import Enum

class InvoiceStatus(str, Enum):
    PENDING_UPLOAD = "PENDING_UPLOAD"
    PROCESSING = "PROCESSING"
    EXTRACTED = "EXTRACTED"
    FAILED = "FAILED"

class InvoiceMetadata(BaseModel):
    invoice_id: str
    s3_key: str
    filename: str
    content_type: str
    status: InvoiceStatus
    uploaded_at: datetime | None
