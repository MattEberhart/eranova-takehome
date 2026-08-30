"use client"

import {ChangeEvent, useEffect, useState } from "react";
import {
  createInvoice, getInvoice, listInvoices,
} from "../lib/api"
import { InvoiceMetadata } from "@/types/Invoice";
import InvoiceDetail from "@/components/InvoiceDetail";
import InvoiceList from "@/components/InvoiceList";
import UploadModal from "@/components/UploadModal";

export default function Home() {

  const [invoices, setInvoices] = useState<InvoiceMetadata[]>([]);
  const [selectedInvoice, setSelectedInvoice] = useState<InvoiceMetadata | null>(null);
  const [documentUrl, setDocumentUrl] = useState<string | null>(null);

  const [uploadOpen, setUploadOpen] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    loadInvoices();
  }, [])

  async function loadInvoices() {
    try
    {
      setLoading(true);
      const data = await listInvoices();

      setInvoices(data);
    } finally
    {
      setLoading(false);
    }
  }

  async function handleUpload() {
    if (!selectedFile) {
      return;
    }

    try
    {
      setUploading(true);

      await createInvoice(selectedFile);

      setSelectedFile(null);
      setUploadOpen(false);

      await loadInvoices();
    }
    catch (error) {
      console.error(error);
      alert("Invoice upload failed")
    }
  }

  async function handleInvoiceClick(invoice: InvoiceMetadata) {
    try 
    {
      const data = await getInvoice(invoice.id);

      setSelectedInvoice(data.invoice);
      setDocumentUrl(data.documentUrl);
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
              onBack={() => {
                setSelectedInvoice(null);
                setDocumentUrl(null);
              }}/>
            ) : (
              <InvoiceList
                invoices={invoices}
                loading={loading}
                onSelect={handleInvoiceClick}
                />
            )}

            {uploadOpen && (
              <UploadModal
                file={selectedFile}
                uploading={uploading}
                onFileChange={handleFileChange}
                onUpload={handleUpload}
                onClose={() => {
                  setUploadOpen(false);
                  setSelectedFile(null);
                }}/>
            )}
            
        </div>
      </main>
  );
}
