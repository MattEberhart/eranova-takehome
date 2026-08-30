import { InvoiceMetadata } from "@/types/Invoice";

type Props = {
  invoices: InvoiceMetadata[];
  loading: boolean;
  onSelect: (invoice: InvoiceMetadata) => void;
};

export default function InvoiceList({
  invoices,
  loading,
  onSelect,
}: Props) {
  if (loading) {
    return <p className="text-zinc-400">Loading invoices...</p>;
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
    <div className="overflow-hidden rounded-xl border border-zinc-800">
      {invoices.map((invoice) => (
        <button
          key={invoice.invoice_id}
          onClick={() => onSelect(invoice)}
          className="flex w-full items-center justify-between border-b border-zinc-800 px-6 py-5 text-left last:border-b-0 hover:bg-zinc-900"
        >
          <div>
            <p className="font-medium">{invoice.filename}</p>

            <p className="mt-1 text-sm text-zinc-500">
              {new Date(invoice.uploaded_at).toLocaleString()}
            </p>
          </div>

          <span className="rounded-full bg-zinc-800 px-3 py-1 text-xs">
            {invoice.status}
          </span>
        </button>
      ))}
    </div>
  );
}