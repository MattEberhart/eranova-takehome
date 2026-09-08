export type InvoiceExtraction = {
    extraction_id: string;
    invoice_metadata_id: string;
    line_items: TaxedLineItem[]
}

export type TaxedLineItem = {
    tax_rate: number;
    tax_amount: number;
    category: string;
    quantity: number;
    item_price: number;
    description: string;
    total_amount: number;
}