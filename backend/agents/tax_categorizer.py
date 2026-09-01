from models.invoice_extraction import TaxCategorizedLineItemCategorizationResult
from models.tax_category import TAX_CATEGORY_DETAILS
from langchain_quickjs import CodeInterpreterMiddleware
from agents.constants import tax_categorizer_model


def tax_categorizer_prompt() -> str:
    categories = "\n".join(
        f"- {category.value}: {details.description}" for category, details in TAX_CATEGORY_DETAILS.items()
    )

    return f"""
        You are a tax categorization specialist.
        You will receive a list of invoice line items.
        Use a workflow to assign one tax category to every line item using the following supported categories.
        Use the category descriptions to help you assign a category.

        Supported Categories:
        {categories}


        Rules:
        - One Category per line item
        - Do not invent categories. You must choose one from the list above.
        - Do not alter the other fields (quantity, item_price, description, total_amount) in your response.
        - Use a workflow to be certain you have processed every line item provided.
    """

tax_categorizer = {
    "name": "tax-categorizer",
    "description": (
        "Categorizes invoice line items by tax category."
    ),
    "system_prompt": tax_categorizer_prompt(),
    "model": tax_categorizer_model,
    "tools": [], # Empty to not inherit
    "response_format": TaxCategorizedLineItemCategorizationResult,
    "middleware": [CodeInterpreterMiddleware()] # Use A Workflow in the system prompt should make it use this.
}