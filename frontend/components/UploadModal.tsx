import { ChangeEvent } from "react";

type Props = {
  file: File | null;
  uploading: boolean;
  uploadingFailed: boolean;
  onFileChange: (event: ChangeEvent<HTMLInputElement>) => void;
  onUpload: () => void;
  onClose: () => void;
};

export default function UploadModal({
  file,
  uploading,
  uploadingFailed,
  onFileChange,
  onUpload,
  onClose,
}: Props) {
  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black/70 px-4">
      <div className="w-full max-w-lg rounded-xl border border-zinc-800 bg-zinc-950 p-6">
        <h2 className="text-xl font-semibold">
          Upload invoice
        </h2>

        <p className="mt-1 text-sm text-zinc-400">
          Choose an invoice document to upload.
        </p>

        <label className="mt-6 flex cursor-pointer flex-col items-center justify-center rounded-xl border border-dashed border-zinc-700 px-6 py-14">
          <span className="font-medium">
            {file ? file.name : "Choose an invoice"}
          </span>

          <span className="mt-2 text-sm text-zinc-500">
            Invoice of any file type!
          </span>

          <input
            type="file"
            onChange={onFileChange}
            className="hidden"
          />
        </label>

        {(uploadingFailed) && (
          <div>
            UPLOAD FAILED
          </div>)}

        <div className="mt-6 flex justify-end gap-3">
          <button
            onClick={onClose}
            disabled={uploading}
            className="rounded-lg px-4 py-2 text-zinc-400"
          >
            Cancel
          </button>

          <button
            onClick={onUpload}
            disabled={!file || uploading}
            className="rounded-lg bg-white px-4 py-2 font-medium text-black disabled:opacity-40"
          >
            {uploading ? "Uploading..." : "Upload"}
          </button>
        </div>
      </div>
    </div>
  );
}