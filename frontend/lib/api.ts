import {InvoiceMetadata} from "../types/Invoice";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function listInvoices(): Promise<InvoiceMetadata[]> {
    var response = await fetch(`${API_URL}/invoices`);

    if (!response.ok)
    {
        console.log(response)
        throw new Error("Failed to fetch invoices")
    }

    const data = await response.json();

    return data.invoices
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

    if (!response)
    {
        throw new Error("Failed to create invoice table record.")
    }

    var data = await response.json();
    
    var uploadResponse = await fetch(data.uploadUrl, {
        method: "PUT",
        headers: {
            "Content-Type": file.type || "application/octet-stream",
        },
        body: file,
    })

    if (!uploadResponse.ok)
    {
        throw new Error("Failed to upload to s3 with upload url")
    }

    return data.invoice

}

export async function getInvoice(id: string): Promise<{
    invoice: InvoiceMetadata;
    documentUrl: string;
}> {
    var response = await fetch(`${API_URL}/invoices/${id}`);

    if (!response.ok)
    {
        throw new Error("Failed to fetch invoice by id.");
    }

    return response.json();
}