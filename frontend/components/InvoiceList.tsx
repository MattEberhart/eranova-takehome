import { listInvoices } from "@/lib/api";
import { InvoiceMetadata, InvoicePage } from "@/types/Invoice";
import {ChangeEvent, useEffect, useState } from "react";

type Props = {
  first_page: InvoicePage;
  onSelect: (invoice: InvoiceMetadata) => void;
};

export default function InvoiceList({
  first_page,
  onSelect,
}: Props) {

  const [invoices, setInvoices] = useState<InvoiceMetadata[]>(first_page.invoices);
  const [cursor, setCursor] = useState<string | null>(first_page.next_cursor)
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    setInvoices(first_page.invoices);
    setCursor(first_page.next_cursor);
  }, [first_page])

  async function loadMoreInvoices() {
    setLoading(true);
    var nextPage = await listInvoices(
      cursor,
      20,
      "desc"
    );

    setInvoices((currentInvoices) => {
      return [...currentInvoices, ...nextPage.invoices]
    })

    setCursor(nextPage.next_cursor);
    setLoading(false)

  }

  if (!invoices || invoices.length === 0) {
    return (
      <div className="rounded-xl border border-zinc-800 p-12 text-center">
        <h2 className="text-lg font-medium">No invoices yet</h2>

        <p className="mt-2 text-sm text-zinc-400">
          Upload your first invoice to get started.
        </p>
      </div>
    );
  }

  return (
    <div>
      <div className="overflow-hidden rounded-xl border border-zinc-800">
        {invoices.map((invoice) => (
          <button
            key={invoice.invoice_id}
            onClick={() => onSelect(invoice)}
            className="flex w-full items-center justify-between border-b border-zinc-800 px-6 py-5 text-left last:border-b-0 hover:bg-zinc-900"
          >
            <div>
              <p className="font-medium">{invoice.filename}</p>

              {(invoice.uploaded_at && <p className="mt-1 text-sm text-zinc-500">
                {new Date(invoice.uploaded_at).toLocaleString()}
              </p>)}
            </div>

            <span className="rounded-full bg-zinc-800 px-3 py-1 text-xs">
              {invoice.status}
            </span>
          </button>
        ))}
      </div>

      {cursor && (
        <button
          type="button"
          disabled={loading}
          onClick={loadMoreInvoices}
          className="mt-4 rounded-lg bg-zinc-800 px-4 py-2 disabled:opacity-50">
        {loading ? "Loading..." : "Load more"}
      </button>
      )}
    </div>

  );
}