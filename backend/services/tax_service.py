## Making this a Service Because Tax Data / Rules Would Eventually Be Stored / Versioned

from models.tax_category import TaxCategory, TaxCategoryDetails, TAX_CATEGORY_DETAILS

class TaxService:

    def __init__(self):
        return
    
    def get_tax_category_details(tax_category:TaxCategory) -> TaxCategoryDetails:
        return TAX_CATEGORY_DETAILS[tax_category]
