import { InvoiceMetadata } from "@/types/Invoice";

type Props = {
  invoice: InvoiceMetadata;
  documentUrl: string | null;
  onBack: () => void;
};

export default function InvoiceDetail({
  invoice,
  documentUrl,
  onBack,
}: Props) {
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
                {new Date(invoice.createdAt).toLocaleString()}
              </dd>
            </div>

            <div>
              <dt className="text-xs uppercase text-zinc-500">
                Invoice ID
              </dt>

              <dd className="mt-1 break-all text-sm text-zinc-400">
                {invoice.id}
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
    </div>
  );
}