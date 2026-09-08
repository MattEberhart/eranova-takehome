import { InvoiceMetadata } from "@/types/Invoice";
import { InvoiceExtraction } from "@/types/InvoiceExtraction";

type Props = {
  invoice: InvoiceMetadata;
  documentUrl: string | null;
  invoiceExtraction: InvoiceExtraction| null;
  onBack: () => void;
};

export default function InvoiceDetail({
  invoice,
  documentUrl,
  invoiceExtraction,
  onBack,
}: Props) {

  var lineItems = invoiceExtraction?.line_items ?? [];
  var subtotal = lineItems.reduce((sum, item) => sum + item.total_amount, 0);
  var totalTax = lineItems.reduce((sum, item) => sum + item.tax_amount, 0);
  var total = subtotal + totalTax;


  return (
    <div>
      <button
        onClick={onBack}
        className="mb-6 text-sm text-zinc-400 hover:text-white"
      >
        ← Back to invoices
      </button>

      <div className="grid min-h-[700px] grid-cols-1 gap-6 lg:grid-cols-[320px_1fr]">
        <aside className="rounded-xl border border-zinc-800 p-6">
          <h2 className="text-lg font-semibold">
            {invoice.filename}
          </h2>

          <dl className="mt-8 space-y-6">
            <div>
              <dt className="text-xs uppercase text-zinc-500">
                Status
              </dt>

              <dd className="mt-1">{invoice.status}</dd>
            </div>

            <div>
              <dt className="text-xs uppercase text-zinc-500">
                Uploaded
              </dt>

              <dd className="mt-1">
                {new Date(invoice.uploaded_at).toLocaleString()}
              </dd>
            </div>

            <div>
              <dt className="text-xs uppercase text-zinc-500">
                Invoice ID
              </dt>

              <dd className="mt-1 break-all text-sm text-zinc-400">
                {invoice.invoice_id}
              </dd>
            </div>
          </dl>
        </aside>

        <section className="overflow-hidden rounded-xl border border-zinc-800 bg-zinc-950">
          {documentUrl ? (
            <iframe
              src={documentUrl}
              title={invoice.filename}
              className="h-full min-h-[700px] w-full"
            />
          ) : (
            <div className="flex min-h-[700px] items-center justify-center text-zinc-500">
              Loading document...
            </div>
          )}
        </section>
      </div>

      {invoiceExtraction ? (
        <>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-zinc-900 text-sx uppercase text-zinc-500">
              <tr>
                <th className="px-6 py-3">Description</th>
                <th className="px-6 py-3">Category</th>
                <th className="px-6 py-3 text-right">Qty</th>
                <th className="px-6 py-3 text-right">Unit price</th>
                <th className="px-6 py-3 text-right">Subtotal</th>
                <th className="px-6 py-3 text-right">Tax rate</th>
                <th className="px-6 py-3 text-right">Tax</th>
                <th className="px-6 py-3 text-right">Total</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-800">
              {lineItems.map((item, index) => {
                const lineTotal = item.total_amount + item.tax_amount;
                return (
                  <tr key={`${item.description}-${index}`}>
                    <td className="max-w-sm px-6 py-4 font-medium">
                      {item.description}
                    </td>
                    <td className="px-6 py-4">
                      <span className="whitespace-nowrap rounded-full bg-zinc-800 px-2.5 py-1 text-xs text-zinc-300">
                        {item.category}
                      </span>
                    </td>

                    <td className="px-6 py-4 text-right tabular-nums">
                      {item.quantity}
                    </td>

                    <td className="px-6 py-4 text-right tabular-nums">
                      {item.item_price}
                    </td>

                    <td className="px-6 py-4 text-right tabular-nums">
                      {item.total_amount}
                    </td>

                    <td className="px-6 py-4 text-right tabular-nums">
                      {(item.tax_rate * 100)}%
                    </td>

                    <td className="px-6 py-4 text-right tabular-nums">
                      {item.tax_amount}
                    </td>

                    <td className="px-6 py-4 text-right font-medium tabular-nums">
                      {lineTotal}
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
          </div>

          <div className="flex justify-end border-t border-zinc-800 bg-zinc-900/50 px-6 py-5">
              <dl className="w-full max-w-xs space-y-3">
                <div className="flex justify-between text-sm">
                  <dt className="text-zinc-400">Subtotal</dt>
                  <dd className="tabular-nums">
                    {subtotal}
                  </dd>
                </div>

                <div className="flex justify-between text-sm">
                  <dt className="text-zinc-400">Tax</dt>
                  <dd className="tabular-nums">
                    {totalTax}
                  </dd>
                </div>

                <div className="flex justify-between border-t border-zinc-700 pt-3 font-semibold">
                  <dt>Total</dt>
                  <dd className="tabular-nums">
                    {total}
                  </dd>
                </div>
              </dl>
            </div>
        </>
      ): (
        <div className="px-6 py-12 text-center text-sm text-zinc-500">
          {invoiceExtraction ? "No line items were extracted." :
          invoice.status === "PROCESSING" ? "The invoice is still being processed." :
          "No extraction data is available for this invoice."}
          </div>
      )}
    </div>
  );
}