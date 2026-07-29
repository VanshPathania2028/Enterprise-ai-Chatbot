import {
  useCallback,
  useEffect,
  useState,
} from "react";

import {
  FileText,
  Loader2,
  RefreshCw,
  Trash2,
  X,
  XCircle,
} from "lucide-react";

import {
  deleteDocument,
  getDocuments,
} from "../api/api";

function DocumentManager({ onClose }) {
  const [documents, setDocuments] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [errorMessage, setErrorMessage] =
    useState("");

  const [
    deletingFilename,
    setDeletingFilename,
  ] = useState("");

  const [
    confirmFilename,
    setConfirmFilename,
  ] = useState("");

  const loadDocuments =
    useCallback(async () => {
      setLoading(true);
      setErrorMessage("");

      try {
        const data =
          await getDocuments();

        let documentList = [];

        if (Array.isArray(data)) {
          documentList = data;
        } else if (
          Array.isArray(data.documents)
        ) {
          documentList =
            data.documents;
        } else if (
          Array.isArray(data.files)
        ) {
          documentList = data.files;
        }

        setDocuments(documentList);
      } catch (error) {
        console.error(
          "Unable to load documents:",
          error
        );

        const backendMessage =
          error.response?.data?.detail ||
          error.response?.data?.message ||
          error.message ||
          "Unable to load documents.";

        setErrorMessage(
          typeof backendMessage ===
            "string"
            ? backendMessage
            : "Unable to load documents."
        );
      } finally {
        setLoading(false);
      }
    }, []);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      void loadDocuments();
    }, 0);

    return () => {
      window.clearTimeout(timer);
    };
  }, [loadDocuments]);

  const getFilename = (document) => {
    if (typeof document === "string") {
      return document;
    }

    return (
      document.filename ||
      document.name ||
      document.file_name ||
      document.original_filename ||
      "Unknown document"
    );
  };

  const getDocumentId = (document) => {
    if (typeof document === "string") {
      return document;
    }

    return (
      document.saved_filename ||
      document.filename ||
      document.name ||
      document.file_name ||
      document.original_filename ||
      ""
    );
  };

  const getChunkCount = (document) => {
    if (
      typeof document !== "object" ||
      document === null
    ) {
      return null;
    }

    return (
      document.chunks ??
      document.chunk_count ??
      document.total_chunks ??
      document.chunks_added ??
      null
    );
  };

  const getFileSize = (document) => {
    if (
      typeof document !== "object" ||
      document === null
    ) {
      return null;
    }

    return (
      document.size ??
      document.file_size ??
      document.size_bytes ??
      null
    );
  };

  const formatFileSize = (size) => {
    if (
      size === null ||
      size === undefined
    ) {
      return "";
    }

    if (typeof size === "string") {
      return size;
    }

    if (size < 1024) {
      return `${size} bytes`;
    }

    if (size < 1024 * 1024) {
      return `${(
        size / 1024
      ).toFixed(2)} KB`;
    }

    return `${(
      size /
      (1024 * 1024)
    ).toFixed(2)} MB`;
  };

  const handleDelete = async (
    filename
  ) => {
    if (!filename) {
      return;
    }

    setDeletingFilename(filename);
    setErrorMessage("");

    try {
      await deleteDocument(filename);

      setDocuments(
        (previousDocuments) =>
          previousDocuments.filter(
            (document) =>
              getDocumentId(document) !==
              filename
          )
      );

      setConfirmFilename("");
    } catch (error) {
      console.error(
        "Document deletion failed:",
        error
      );

      const backendMessage =
        error.response?.data?.detail ||
        error.response?.data?.message ||
        error.message ||
        "Unable to delete document.";

      setErrorMessage(
        typeof backendMessage ===
          "string"
          ? backendMessage
          : "Unable to delete document."
      );
    } finally {
      setDeletingFilename("");
    }
  };

  const handleBackdropClick = (
    event
  ) => {
    if (
      event.target ===
      event.currentTarget
    ) {
      onClose();
    }
  };

  return (
    <div
      className="fixed inset-0 flex items-center justify-center bg-black/70 p-4 backdrop-blur-sm"
      style={{ zIndex: 80 }}
      onMouseDown={
        handleBackdropClick
      }
      role="presentation"
    >
      <div
        className="flex max-h-[85vh] w-full max-w-2xl flex-col overflow-hidden rounded-2xl border border-slate-700 bg-slate-900 shadow-2xl"
        onMouseDown={(event) =>
          event.stopPropagation()
        }
        role="dialog"
        aria-modal="true"
        aria-labelledby="documents-title"
      >
        <div className="flex shrink-0 items-center justify-between border-b border-slate-800 px-5 py-4">
          <div>
            <h2
              id="documents-title"
              className="text-lg font-semibold text-white"
            >
              Document Manager
            </h2>

            <p className="mt-1 text-xs text-slate-400">
              View and manage indexed
              knowledge-base documents.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={loadDocuments}
              disabled={loading}
              className="rounded-lg p-2 text-slate-400 transition hover:bg-slate-800 hover:text-white disabled:cursor-not-allowed disabled:opacity-50"
              aria-label="Refresh documents"
            >
              <RefreshCw
                size={19}
                className={
                  loading
                    ? "animate-spin"
                    : ""
                }
              />
            </button>

            <button
              type="button"
              onClick={onClose}
              className="rounded-lg p-2 text-slate-400 transition hover:bg-slate-800 hover:text-white"
              aria-label="Close document manager"
            >
              <X size={20} />
            </button>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-5">
          {errorMessage && (
            <div className="mb-4 flex items-start gap-3 rounded-xl border border-red-500/30 bg-red-950/50 p-4 text-sm text-red-200">
              <XCircle
                size={19}
                className="mt-0.5 shrink-0"
              />

              <span>
                {errorMessage}
              </span>
            </div>
          )}

          {loading ? (
            <div className="flex min-h-60 flex-col items-center justify-center text-slate-400">
              <Loader2
                size={34}
                className="animate-spin text-blue-400"
              />

              <p className="mt-4 text-sm">
                Loading documents...
              </p>
            </div>
          ) : documents.length === 0 ? (
            <div className="flex min-h-60 flex-col items-center justify-center rounded-2xl border border-dashed border-slate-700 bg-slate-800/30 p-8 text-center">
              <div className="flex h-14 w-14 items-center justify-center rounded-full bg-slate-800 text-slate-400">
                <FileText size={27} />
              </div>

              <h3 className="mt-4 font-medium text-white">
                No documents found
              </h3>

              <p className="mt-2 max-w-sm text-sm text-slate-400">
                Upload a PDF to add it
                to the enterprise
                knowledge base.
              </p>
            </div>
          ) : (
            <div className="space-y-3">
              {documents.map(
                (document, index) => {
                  const filename =
                    getFilename(document);

                  const documentId =
                    getDocumentId(document);

                  const chunkCount =
                    getChunkCount(
                      document
                    );

                  const fileSize =
                    getFileSize(
                      document
                    );

                  const isDeleting =
                    deletingFilename ===
                    documentId;

                  const isConfirming =
                    confirmFilename ===
                    documentId;

                  return (
                    <div
                      key={`${documentId}-${index}`}
                      className="rounded-xl border border-slate-700 bg-slate-800/70 p-4"
                    >
                      <div className="flex items-start gap-3">
                        <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg bg-red-500/15 text-red-400">
                          <FileText
                            size={22}
                          />
                        </div>

                        <div className="min-w-0 flex-1">
                          <p
                            className="truncate text-sm font-medium text-white"
                            title={
                              filename
                            }
                          >
                            {filename}
                          </p>

                          <div className="mt-2 flex flex-wrap gap-2 text-xs text-slate-400">
                            {chunkCount !==
                              null && (
                              <span className="rounded-md bg-slate-700 px-2 py-1">
                                {chunkCount}{" "}
                                {Number(
                                  chunkCount
                                ) === 1
                                  ? "chunk"
                                  : "chunks"}
                              </span>
                            )}

                            {fileSize !==
                              null && (
                              <span className="rounded-md bg-slate-700 px-2 py-1">
                                {formatFileSize(
                                  fileSize
                                )}
                              </span>
                            )}

                            <span className="rounded-md bg-green-500/10 px-2 py-1 text-green-400">
                              Indexed
                            </span>
                          </div>
                        </div>

                        <button
                          type="button"
                          onClick={() =>
                            setConfirmFilename(
                              documentId
                            )
                          }
                          disabled={
                            isDeleting
                          }
                          className="rounded-lg p-2 text-slate-400 transition hover:bg-red-500/10 hover:text-red-400 disabled:cursor-not-allowed disabled:opacity-50"
                          aria-label={`Delete ${filename}`}
                        >
                          {isDeleting ? (
                            <Loader2
                              size={18}
                              className="animate-spin"
                            />
                          ) : (
                            <Trash2
                              size={18}
                            />
                          )}
                        </button>
                      </div>

                      {isConfirming && (
                        <div className="mt-4 rounded-xl border border-red-500/30 bg-red-950/30 p-4">
                          <p className="text-sm text-red-200">
                            Delete{" "}
                            <span className="font-semibold">
                              {filename}
                            </span>
                            ?
                          </p>

                          <p className="mt-1 text-xs text-red-300/70">
                            The document and
                            its indexed chunks
                            will be removed.
                          </p>

                          <div className="mt-3 flex justify-end gap-2">
                            <button
                              type="button"
                              onClick={() =>
                                setConfirmFilename(
                                  ""
                                )
                              }
                              disabled={
                                isDeleting
                              }
                              className="rounded-lg border border-slate-600 px-3 py-2 text-xs font-medium text-slate-300 transition hover:bg-slate-700 disabled:opacity-50"
                            >
                              Cancel
                            </button>

                            <button
                              type="button"
                              onClick={() =>
                                handleDelete(
                                  documentId
                                )
                              }
                              disabled={
                                isDeleting
                              }
                              className="flex items-center gap-2 rounded-lg bg-red-600 px-3 py-2 text-xs font-medium text-white transition hover:bg-red-500 disabled:cursor-not-allowed disabled:opacity-50"
                            >
                              {isDeleting ? (
                                <Loader2
                                  size={14}
                                  className="animate-spin"
                                />
                              ) : (
                                <Trash2
                                  size={14}
                                />
                              )}

                              {isDeleting
                                ? "Deleting..."
                                : "Delete"}
                            </button>
                          </div>
                        </div>
                      )}
                    </div>
                  );
                }
              )}
            </div>
          )}
        </div>

        <div className="flex shrink-0 items-center justify-between border-t border-slate-800 px-5 py-4">
          <p className="text-xs text-slate-400">
            {documents.length}{" "}
            {documents.length === 1
              ? "document"
              : "documents"}
          </p>

          <button
            type="button"
            onClick={onClose}
            className="rounded-xl border border-slate-700 px-5 py-2.5 text-sm font-medium text-slate-300 transition hover:bg-slate-800 hover:text-white"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

export default DocumentManager;
