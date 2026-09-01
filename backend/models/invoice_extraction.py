from datetime import datetime
from pydantic import BaseModel
from decimal import Decimal
from enum import Enum
from models.tax_category import TaxCategory

class LineItem(BaseModel):
    # Extraction Agent Sets These
    quantity: int
    item_price: float
    description: str
    total_amount: float


# Need pydantic type to enfore response_format in extractor agent.
# list[LineItem] would not have worked.
class LineItemExtractionResult(BaseModel):
    line_items: list[LineItem]

class TaxCategorizedLineItem(LineItem):
    # Categorzier Agent Sets This
    category: TaxCategory

## Same idea as above, need pydantic type with list of items
class TaxCategorizedLineItemCategorizationResult(BaseModel):
    line_items: list[TaxCategorizedLineItem]

class TaxedLineItem(TaxCategorizedLineItem):
    # Set Deterministically After Categorized
    item_price: Decimal ## Override LineItem float that was used for extraction
    total_amount: Decimal ## Override LineItem float that was used for extraciton
    tax_rate: Decimal
    tax_amount: Decimal

class InvoiceExtraction(BaseModel):
    invoice_extraction_id: str
    invoice_metadata_id: str
    line_items: list[TaxedLineItem]
