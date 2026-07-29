import { useRef, useState } from "react";
import {
  CheckCircle2,
  FileText,
  Upload,
  X,
  XCircle,
} from "lucide-react";

import { uploadDocument } from "../api/api";

function UploadDocument({
  onClose,
  onUploadSuccess,
}) {
  const [selectedFile, setSelectedFile] =
    useState(null);

  const [uploading, setUploading] =
    useState(false);

  const [uploadProgress, setUploadProgress] =
    useState(0);

  const [errorMessage, setErrorMessage] =
    useState("");

  const [successMessage, setSuccessMessage] =
    useState("");

  const fileInputRef = useRef(null);

  const validateFile = (file) => {
    if (!file) {
      return "Please select a PDF file.";
    }

    const isPdf =
      file.type === "application/pdf" ||
      file.name
        .toLowerCase()
        .endsWith(".pdf");

    if (!isPdf) {
      return "Only PDF files are allowed.";
    }

    const maximumSize =
      10 * 1024 * 1024;

    if (file.size > maximumSize) {
      return "PDF size must be less than 10 MB.";
    }

    return "";
  };

  const selectFile = (file) => {
    setErrorMessage("");
    setSuccessMessage("");
    setUploadProgress(0);

    const validationMessage =
      validateFile(file);

    if (validationMessage) {
      setSelectedFile(null);
      setErrorMessage(
        validationMessage
      );

      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }

      return;
    }

    setSelectedFile(file);
  };

  const handleFileChange = (event) => {
    const file =
      event.target.files?.[0];

    selectFile(file);
  };

  const handleDrop = (event) => {
    event.preventDefault();

    if (uploading) {
      return;
    }

    const file =
      event.dataTransfer.files?.[0];

    selectFile(file);
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const handleUpload = async () => {
    const validationMessage =
      validateFile(selectedFile);

    if (validationMessage) {
      setErrorMessage(
        validationMessage
      );
      return;
    }

    setUploading(true);
    setUploadProgress(0);
    setErrorMessage("");
    setSuccessMessage("");

    try {
      const result =
        await uploadDocument(
          selectedFile,
          (progressEvent) => {
            if (
              !progressEvent.total
            ) {
              return;
            }

            const percentage =
              Math.round(
                (progressEvent.loaded *
                  100) /
                  progressEvent.total
              );

            setUploadProgress(
              percentage
            );
          }
        );

      setUploadProgress(100);

      const chunksAdded =
        result?.chunks_added;

      const message =
        chunksAdded !== undefined
          ? `Document uploaded and indexed successfully. ${chunksAdded} chunks added.`
          : result?.message ||
            "Document uploaded successfully.";

      setSuccessMessage(message);

      setSelectedFile(null);

      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }

      setTimeout(() => {
        if (
          typeof onUploadSuccess ===
          "function"
        ) {
          onUploadSuccess(result);
        } else {
          onClose();
        }
      }, 1000);
    } catch (error) {
      console.error(
        "Document upload failed:",
        error
      );

      const backendMessage =
        error.response?.data?.detail ||
        error.response?.data?.message ||
        error.message ||
        "Unable to upload the document.";

      setErrorMessage(
        typeof backendMessage ===
          "string"
          ? backendMessage
          : "Unable to upload the document."
      );

      setUploadProgress(0);
    } finally {
      setUploading(false);
    }
  };

  const removeSelectedFile = () => {
    if (uploading) {
      return;
    }

    setSelectedFile(null);
    setErrorMessage("");
    setSuccessMessage("");
    setUploadProgress(0);

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const formatFileSize = (
    numberOfBytes
  ) => {
    if (!numberOfBytes) {
      return "0 KB";
    }

    const sizeInMegabytes =
      numberOfBytes /
      (1024 * 1024);

    if (sizeInMegabytes >= 1) {
      return `${sizeInMegabytes.toFixed(
        2
      )} MB`;
    }

    const sizeInKilobytes =
      numberOfBytes / 1024;

    return `${sizeInKilobytes.toFixed(
      2
    )} KB`;
  };

  const handleClose = () => {
    if (!uploading) {
      onClose();
    }
  };

  return (
    <div
      className="fixed inset-0 flex items-center justify-center bg-black/70 p-4 backdrop-blur-sm"
      style={{ zIndex: 70 }}
    >
      <div className="w-full max-w-lg overflow-hidden rounded-2xl border border-slate-700 bg-slate-900 shadow-2xl">
        <div className="flex items-center justify-between border-b border-slate-800 px-5 py-4">
          <div>
            <h2 className="text-lg font-semibold text-white">
              Upload document
            </h2>

            <p className="mt-1 text-xs text-slate-400">
              Upload a PDF to your
              enterprise knowledge base.
            </p>
          </div>

          <button
            type="button"
            onClick={handleClose}
            disabled={uploading}
            className="rounded-lg p-2 text-slate-400 transition hover:bg-slate-800 hover:text-white disabled:cursor-not-allowed disabled:opacity-50"
            aria-label="Close upload window"
          >
            <X size={20} />
          </button>
        </div>

        <div className="space-y-5 p-5">
          <div
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onClick={() => {
              if (!uploading) {
                fileInputRef.current?.click();
              }
            }}
            className={`cursor-pointer rounded-2xl border-2 border-dashed p-8 text-center transition ${
              selectedFile
                ? "border-blue-500 bg-blue-500/5"
                : "border-slate-700 hover:border-blue-500 hover:bg-slate-800/50"
            } ${
              uploading
                ? "cursor-not-allowed opacity-60"
                : ""
            }`}
            role="button"
            tabIndex={0}
            onKeyDown={(event) => {
              if (
                event.key === "Enter" ||
                event.key === " "
              ) {
                event.preventDefault();

                if (!uploading) {
                  fileInputRef.current?.click();
                }
              }
            }}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,application/pdf"
              onChange={handleFileChange}
              disabled={uploading}
              className="hidden"
            />

            <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-blue-600/20 text-blue-400">
              <Upload size={27} />
            </div>

            <p className="mt-4 font-medium text-white">
              Click to choose a PDF
            </p>

            <p className="mt-1 text-sm text-slate-400">
              or drag and drop it here
            </p>

            <p className="mt-3 text-xs text-slate-500">
              Maximum file size: 10 MB
            </p>
          </div>

          {selectedFile && (
            <div className="flex items-center gap-3 rounded-xl border border-slate-700 bg-slate-800 p-4">
              <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg bg-red-500/15 text-red-400">
                <FileText size={22} />
              </div>

              <div className="min-w-0 flex-1">
                <p className="truncate text-sm font-medium text-white">
                  {selectedFile.name}
                </p>

                <p className="mt-1 text-xs text-slate-400">
                  {formatFileSize(
                    selectedFile.size
                  )}
                </p>
              </div>

              <button
                type="button"
                onClick={(event) => {
                  event.stopPropagation();
                  removeSelectedFile();
                }}
                disabled={uploading}
                className="rounded-lg p-2 text-slate-400 transition hover:bg-slate-700 hover:text-red-400 disabled:cursor-not-allowed disabled:opacity-50"
                aria-label="Remove selected file"
              >
                <X size={18} />
              </button>
            </div>
          )}

          {uploading && (
            <div className="rounded-xl border border-slate-700 bg-slate-800 p-4">
              <div className="mb-2 flex items-center justify-between text-sm">
                <span className="text-slate-300">
                  Uploading and indexing...
                </span>

                <span className="font-medium text-blue-400">
                  {uploadProgress}%
                </span>
              </div>

              <div className="h-2 overflow-hidden rounded-full bg-slate-700">
                <div
                  className="h-full rounded-full bg-blue-600 transition-all duration-300"
                  style={{
                    width: `${uploadProgress}%`,
                  }}
                />
              </div>

              <p className="mt-2 text-xs text-slate-500">
                Do not close this window
                while the document is being
                processed.
              </p>
            </div>
          )}

          {successMessage && (
            <div className="flex items-start gap-3 rounded-xl border border-green-500/30 bg-green-950/50 p-4 text-sm text-green-200">
              <CheckCircle2
                size={19}
                className="mt-0.5 shrink-0"
              />

              <span>
                {successMessage}
              </span>
            </div>
          )}

          {errorMessage && (
            <div className="flex items-start gap-3 rounded-xl border border-red-500/30 bg-red-950/50 p-4 text-sm text-red-200">
              <XCircle
                size={19}
                className="mt-0.5 shrink-0"
              />

              <span>
                {errorMessage}
              </span>
            </div>
          )}
        </div>

        <div className="flex justify-end gap-3 border-t border-slate-800 px-5 py-4">
          <button
            type="button"
            onClick={handleClose}
            disabled={uploading}
            className="rounded-xl border border-slate-700 px-5 py-2.5 text-sm font-medium text-slate-300 transition hover:bg-slate-800 hover:text-white disabled:cursor-not-allowed disabled:opacity-50"
          >
            Cancel
          </button>

          <button
            type="button"
            onClick={handleUpload}
            disabled={
              !selectedFile ||
              uploading ||
              Boolean(successMessage)
            }
            className="flex items-center gap-2 rounded-xl bg-blue-600 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
          >
            <Upload size={17} />

            {uploading
              ? "Uploading..."
              : "Upload PDF"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default UploadDocument;
