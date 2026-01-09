"use client";

import { useState } from "react";

interface UploadDropzoneProps {
  conversionType: string;
}

export function UploadDropzone({ conversionType }: UploadDropzoneProps) {
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState("Ready to upload");

  const handleUpload = () => {
    setStatus("Uploading...");
    setProgress(35);
    setTimeout(() => {
      setProgress(100);
      setStatus("Processing in background");
    }, 600);
  };

  return (
    <div className="rounded-3xl border-2 border-dashed border-slate-300 bg-white p-10 text-center shadow-sm">
      <h2 className="text-2xl font-semibold text-slate-900">{conversionType}</h2>
      <p className="mt-2 text-sm text-slate-500">
        Drag & drop your file or click to upload. We&apos;ll handle the conversion in seconds.
      </p>
      <div className="mt-6">
        <button
          type="button"
          onClick={handleUpload}
          className="rounded-full bg-primary-600 px-6 py-3 text-sm font-semibold text-white hover:bg-primary-500"
        >
          Upload file
        </button>
      </div>
      <div className="mt-6">
        <div className="h-2 w-full overflow-hidden rounded-full bg-slate-100">
          <div className="h-full bg-primary-600" style={{ width: `${progress}%` }} />
        </div>
        <p className="mt-2 text-xs text-slate-500">{status}</p>
      </div>
    </div>
  );
}
