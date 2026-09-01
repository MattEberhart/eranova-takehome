from langchain.tools import tool
from models.tax_category import TaxCategory, TaxCategoryDetails
from services.tax_service import TaxService
from models.invoice_extraction import TaxCategorizedLineItemCategorizationResult, TaxedLineItem

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
        category_details:TaxCategoryDetails = service.get_tax_category_details(line_item.category)

        tax_amount = category_details.tax_rate * line_item.total_amount

        taxed_line_item = TaxedLineItem(
            quantity=line_item.quantity,
            item_price=line_item.item_price,
            description=line_item.description,
            total_amount=line_item.total_amount,
            tax_rate=category_details.tax_rate,
            tax_amount=tax_amount
        )

        taxed_items.append(taxed_line_item)

    return taxed_items