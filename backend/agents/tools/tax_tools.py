from langchain.tools import tool
from models.tax_category import TaxCategory, TaxCategoryDetails
from services.tax_service import TaxService
from models.invoice_extraction import TaxCategorizedLineItemCategorizationResult, TaxedLineItem
from decimal import Decimal

service = TaxService()

@tool
def calculate_line_item_taxes(
    categorization_result: TaxCategorizedLineItemCategorizationResult) -> list[TaxedLineItem]:
    """
    Calculate tax rates and tax amounts for categorized invoice line items.
    """

    taxed_items:list[TaxedLineItem] = []

    for line_item in categorization_result.line_items:
        category_details = service.get_tax_category_details(line_item.category)

        tax_rate = category_details.tax_rate
        tax_amount = line_item.total_amount * tax_rate

        taxed_line_item = TaxedLineItem(
            **line_item.model_dump(),
            tax_rate=tax_rate,
            tax_amount=tax_amount
        )

        taxed_items.append(taxed_line_item)

    return taxed_items