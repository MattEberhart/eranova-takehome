import { InvoiceExtraction } from "@/types/InvoiceExtraction";
import {InvoiceMetadata, InvoicePage} from "../types/Invoice";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function listInvoices(
    cursor: string | null = null,
    limit: number = 10,
    order: string = "desc"
): Promise<InvoicePage> {

    var params = new URLSearchParams({
        limit: limit.toString(),
        order
    });

    if (cursor)
    {
        params.set("cursor", cursor)
    }

    const response = await fetch(`${API_URL}/invoices?${params.toString()}`);

    if (!response.ok)
    {
        console.log(response)
        throw new Error("Failed to fetch invoices")
    }

    return response.json();
}

export async function createInvoice(file: File): Promise<InvoiceMetadata> {
    console.log(`${API_URL}/invoices`);
    var response = await fetch (`${API_URL}/invoices`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
            filename: file.name,
            contentType: file.type || "application/octet-stream",
            }),
        }
    );

    if (!response || response.status != 201)
    {
        throw new Error("Failed to create invoice table record.")
    }

    var data = await response.json();
    
    var uploadResponse = await fetch(data.upload_url, {
        method: "PUT",
        headers: {
            "Content-Type": file.type || "application/octet-stream",
        },
        body: file,
    })

    if (!uploadResponse.ok)
    {
        throw new Error("Failed to upload to s3 with upload url")
        // We need to delete the orphaned metadata record. Leaving for now,
        // involves delete invoice lambda, service function, etc
    }

    return data.invoice

}

export async function getInvoice(id: string): Promise<{
    invoice_metadata: InvoiceMetadata;
    invoice_document_url: string;
    invoice_extraction: InvoiceExtraction;
}> {
    var response = await fetch(`${API_URL}/invoices/${id}`);

    if (!response.ok)
    {
        throw new Error("Failed to fetch invoice by id.");
    }

    return response.json();
}