from langchain.tools import tool
from models.tax_category import TaxCategory, TaxCategoryDetails
from services.tax_service import TaxService
from models.invoice_extraction import TaxCategorizedLineItemCategorizationResult, TaxedLineItem
from decimal import Decimal, ROUND_HALF_UP

service = TaxService()

@tool
def calculate_line_item_taxes(
    categorization_result: TaxCategorizedLineItemCategorizationResult) -> list[TaxedLineItem]:
    """
    Calculate tax rates and tax amounts for categorized invoice line items.
    """

    # Maybe Move This Logic To Tax Service Later
    # Stuff Like Rounding Rules Would Eventually Come From There as Well
    # This Feels like Too Much Business Logic for a Tool
    # Maybe not because this is a conversion specifically for a TaxCatetgorizedLineItemCategorizationResult
    taxed_items:list[TaxedLineItem] = []

    for line_item in categorization_result.line_items:
        category_details = service.get_tax_category_details(line_item.category)

        # Used Floats for Extraction - Convert to Decimal
        tax_rate = Decimal(str(category_details.tax_rate))
        line_item_total_amount = Decimal(str(line_item.total_amount))

        tax_amount = (line_item_total_amount * tax_rate)
        tax_amount = tax_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        taxed_line_item = TaxedLineItem(
            quantity=line_item.quantity,
            item_price=Decimal(str(line_item.item_price)),
            description=line_item.description,
            total_amount=line_item_total_amount,
            tax_rate=tax_rate,
            tax_amount=tax_amount
        )

        taxed_items.append(taxed_line_item)

    return taxed_items