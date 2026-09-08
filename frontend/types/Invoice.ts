export type InvoiceMetadata = {
    invoice_id: string;
    s3_key: string;
    content_type: string;
    filename: string;
    status: string;
    uploaded_at: string;
};

export type InvoicePage = {
    invoices:InvoiceMetadata[];
    next_cursor:string | null;
}