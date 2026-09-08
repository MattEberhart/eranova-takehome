"use client"

import {ChangeEvent, useEffect, useState } from "react";
import {
  createInvoice, getInvoice, listInvoices,
} from "../lib/api"
import { InvoiceMetadata, InvoicePage } from "@/types/Invoice";
import InvoiceDetail from "@/components/InvoiceDetail";
import InvoiceList from "@/components/InvoiceList";
import UploadModal from "@/components/UploadModal";
import { InvoiceExtraction } from "@/types/InvoiceExtraction";

export default function Home() {

  const [invoices, setInvoices] = useState<InvoicePage>({invoices:[], next_cursor:null});
  const [selectedInvoice, setSelectedInvoice] = useState<InvoiceMetadata | null>(null);
  const [documentUrl, setDocumentUrl] = useState<string | null>(null);
  const [invoiceExtraction, setInvoiceExtraction] = useState<InvoiceExtraction | null>(null);

  const [uploadOpen, setUploadOpen] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const [uploading, setUploading] = useState(false);
  const [uploadingFailed, setUploadingFailed] = useState(false);

  useEffect(() => {
    loadInvoices();
  }, [])

  async function loadInvoices() {
      const data = await listInvoices();
      console.log(data)
      setInvoices(data);
      console.log(invoices)
  }

  async function handleUpload() {
    if (!selectedFile) {
      return;
    }

    try
    {
      setUploading(true);
      setUploadingFailed(false);

      await createInvoice(selectedFile);

      setSelectedFile(null);
      setUploadOpen(false);

      await loadInvoices();
    }
    catch (error) {
      console.error(error);
      alert("Invoice upload failed")
      setUploading(false);
      setUploadingFailed(true);
    }
  }

  async function handleInvoiceClick(invoice: InvoiceMetadata) {
    try 
    {
      const data = await getInvoice(invoice.invoice_id);

      setSelectedInvoice(data.invoice_metadata);
      setDocumentUrl(data.invoice_document_url);
      setInvoiceExtraction(data.invoice_extraction);
    } catch (error)
    {
      console.error(error);
      alert("Failed to load invoice");
    }
  }

  async function handleFileChange(event: ChangeEvent<HTMLInputElement>)
  {
    const file = event.target.files?.[0]

    if (file)
    {
      setSelectedFile(file);
      setUploadingFailed(false);
    }
  }


  return (
      <main className="min-h-screen bg-black text-white">
        <div className="mx-auto max-w-7xl px-8 py-10">
          <header className="mx-auto max-w-7xl px-8 py-10">
            <div className="mb-12 flex items-center justify-between">
              <h1 className="text-3xl font-semibold">Invoices</h1>
            </div>
            <button
              onClick={() => setUploadOpen(true)}
              className="rounded-lg bg-white px-4 py-2 font-medium text-black hover:bg-zinc-200"
              >
                Upload Invoice
              </button>
          </header>

          {selectedInvoice ? (
            <InvoiceDetail
              invoice={selectedInvoice}
              documentUrl={documentUrl}
              invoiceExtraction={invoiceExtraction}
              onBack={() => {
                setSelectedInvoice(null);
                setDocumentUrl(null);
                setInvoiceExtraction(null);
              }}/>
            ) : (
              <InvoiceList
                first_page={invoices}
                onSelect={handleInvoiceClick}
                />
            )}

            {uploadOpen && (
              <UploadModal
                file={selectedFile}
                uploading={uploading}
                uploadingFailed={uploadingFailed}
                onFileChange={handleFileChange}
                onUpload={handleUpload}
                onClose={() => {
                  setUploadOpen(false);
                  setSelectedFile(null);
                  setUploadingFailed(false);
                }}/>
            )}
            
        </div>
      </main>
  );
}
