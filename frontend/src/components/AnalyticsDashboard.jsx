import {
  Activity,
  Bot,
  FileText,
  Loader2,
  MessageSquare,
  RefreshCw,
  Server,
  X,
} from "lucide-react";

import {
  useCallback,
  useEffect,
  useState,
} from "react";

import {
  getDocuments,
} from "../api/api";

function AnalyticsDashboard({
  onClose,
  messages = [],
  backendOnline = false,
}) {
  const [documents, setDocuments] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  const loadAnalytics =
    useCallback(async () => {
      setLoading(true);
      setError("");

      try {
        const data =
          await getDocuments();

        if (Array.isArray(data)) {
          setDocuments(data);
        } else if (
          Array.isArray(data.documents)
        ) {
          setDocuments(
            data.documents
          );
        } else if (
          Array.isArray(data.files)
        ) {
          setDocuments(data.files);
        } else {
          setDocuments([]);
        }
      } catch (requestError) {
        console.error(
          "Unable to load analytics:",
          requestError
        );

        setError(
          requestError.response?.data
            ?.detail ||
            requestError.message ||
            "Unable to load analytics."
        );
      } finally {
        setLoading(false);
      }
    }, []);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      void loadAnalytics();
    }, 0);

    return () => {
      window.clearTimeout(timer);
    };
  }, [loadAnalytics]);

  const totalChunks =
    documents.reduce(
      (total, document) => {
        if (
          typeof document !== "object" ||
          document === null
        ) {
          return total;
        }

        const chunks =
          document.chunks ??
          document.chunk_count ??
          document.total_chunks ??
          document.chunks_added ??
          0;

        return (
          total +
          (Number(chunks) || 0)
        );
      },
      0
    );

  const userMessages =
    messages.filter(
      (message) =>
        message.role === "user"
    ).length;

  const assistantMessages =
    messages.filter(
      (message) =>
        message.role === "assistant"
    ).length;

  const closeOnBackdrop = (
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
      style={{ zIndex: 90 }}
      onMouseDown={
        closeOnBackdrop
      }
      role="presentation"
    >
      <div
        className="flex max-h-[90vh] w-full max-w-5xl flex-col overflow-hidden rounded-2xl border border-slate-700 bg-slate-900 shadow-2xl"
        onMouseDown={(event) =>
          event.stopPropagation()
        }
        role="dialog"
        aria-modal="true"
        aria-labelledby="analytics-title"
      >
        <div className="flex items-center justify-between border-b border-slate-800 px-5 py-4">
          <div>
            <h2
              id="analytics-title"
              className="text-xl font-semibold text-white"
            >
              Analytics Dashboard
            </h2>

            <p className="mt-1 text-sm text-slate-400">
              Monitor documents,
              conversations and system
              status.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={loadAnalytics}
              disabled={loading}
              className="rounded-lg p-2 text-slate-400 transition hover:bg-slate-800 hover:text-white disabled:opacity-50"
              aria-label="Refresh analytics"
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
              aria-label="Close analytics dashboard"
            >
              <X size={20} />
            </button>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-5">
          {error && (
            <div className="mb-5 rounded-xl border border-red-500/30 bg-red-950/40 p-4 text-sm text-red-200">
              {error}
            </div>
          )}

          {loading ? (
            <div className="flex min-h-80 flex-col items-center justify-center text-slate-400">
              <Loader2
                size={36}
                className="animate-spin text-blue-400"
              />

              <p className="mt-4 text-sm">
                Loading analytics...
              </p>
            </div>
          ) : (
            <>
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                <AnalyticsCard
                  title="Documents"
                  value={
                    documents.length
                  }
                  description="Indexed PDF files"
                  icon={FileText}
                />

                <AnalyticsCard
                  title="Chunks"
                  value={totalChunks}
                  description="Knowledge chunks"
                  icon={Activity}
                />

                <AnalyticsCard
                  title="Questions"
                  value={userMessages}
                  description="User messages"
                  icon={
                    MessageSquare
                  }
                />

                <AnalyticsCard
                  title="AI Responses"
                  value={
                    assistantMessages
                  }
                  description="Assistant messages"
                  icon={Bot}
                />
              </div>

              <div className="mt-6 grid gap-4 lg:grid-cols-2">
                <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-5">
                  <h3 className="flex items-center gap-2 font-semibold text-white">
                    <Server
                      size={19}
                      className="text-blue-400"
                    />

                    System status
                  </h3>

                  <div className="mt-5 space-y-4">
                    <StatusRow
                      label="FastAPI backend"
                      status={
                        backendOnline
                          ? "Online"
                          : "Offline"
                      }
                      online={
                        backendOnline
                      }
                    />

                    <StatusRow
                      label="Ollama model"
                      status="llama3.2"
                      online
                    />

                    <StatusRow
                      label="Retrieval mode"
                      status="Hybrid RAG"
                      online
                    />

                    <StatusRow
                      label="Vector database"
                      status="ChromaDB"
                      online
                    />

                    <StatusRow
                      label="Knowledge graph"
                      status="Neo4j"
                      online
                    />
                  </div>
                </div>

                <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-5">
                  <h3 className="flex items-center gap-2 font-semibold text-white">
                    <MessageSquare
                      size={19}
                      className="text-blue-400"
                    />

                    Conversation summary
                  </h3>

                  <div className="mt-5 space-y-4">
                    <ProgressRow
                      label="User messages"
                      value={userMessages}
                      total={Math.max(
                        messages.length,
                        1
                      )}
                    />

                    <ProgressRow
                      label="AI responses"
                      value={
                        assistantMessages
                      }
                      total={Math.max(
                        messages.length,
                        1
                      )}
                    />

                    <ProgressRow
                      label="Indexed documents"
                      value={
                        documents.length
                      }
                      total={Math.max(
                        documents.length,
                        1
                      )}
                    />
                  </div>
                </div>
              </div>

              <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-950/60 p-5">
                <h3 className="font-semibold text-white">
                  Indexed documents
                </h3>

                {documents.length ===
                0 ? (
                  <p className="mt-4 text-sm text-slate-400">
                    No documents have
                    been indexed.
                  </p>
                ) : (
                  <div className="mt-4 grid gap-3 sm:grid-cols-2">
                    {documents.map(
                      (
                        document,
                        index
                      ) => {
                        const filename =
                          typeof document ===
                          "string"
                            ? document
                            : document.filename ||
                              document.name ||
                              document.file_name ||
                              document.original_filename ||
                              `Document ${
                                index +
                                1
                              }`;

                        const chunks =
                          typeof document ===
                          "object" &&
                          document !==
                            null
                            ? document.chunks ??
                              document.chunk_count ??
                              document.total_chunks ??
                              document.chunks_added
                            : null;

                        return (
                          <div
                            key={`${filename}-${index}`}
                            className="flex items-center gap-3 rounded-xl border border-slate-800 bg-slate-900 p-4"
                          >
                            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-red-500/10 text-red-400">
                              <FileText
                                size={
                                  20
                                }
                              />
                            </div>

                            <div className="min-w-0">
                              <p
                                className="truncate text-sm font-medium text-white"
                                title={
                                  filename
                                }
                              >
                                {
                                  filename
                                }
                              </p>

                              <p className="mt-1 text-xs text-slate-400">
                                {chunks !==
                                null
                                  ? `${chunks} chunks`
                                  : "Indexed"}
                              </p>
                            </div>
                          </div>
                        );
                      }
                    )}
                  </div>
                )}
              </div>
            </>
          )}
        </div>

        <div className="flex items-center justify-end border-t border-slate-800 px-5 py-4">
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

function AnalyticsCard({
  title,
  value,
  description,
  icon: Icon,
}) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-5">
      <div className="flex items-center justify-between">
        <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-500/10 text-blue-400">
          <Icon size={21} />
        </div>

        <span className="text-2xl font-bold text-white">
          {value}
        </span>
      </div>

      <h3 className="mt-4 font-semibold text-white">
        {title}
      </h3>

      <p className="mt-1 text-xs text-slate-400">
        {description}
      </p>
    </div>
  );
}

function StatusRow({
  label,
  status,
  online,
}) {
  return (
    <div className="flex items-center justify-between gap-4">
      <span className="text-sm text-slate-400">
        {label}
      </span>

      <span
        className={`flex items-center gap-2 text-sm ${
          online
            ? "text-green-400"
            : "text-red-400"
        }`}
      >
        <span
          className={`h-2 w-2 rounded-full ${
            online
              ? "bg-green-500"
              : "bg-red-500"
          }`}
        />

        {status}
      </span>
    </div>
  );
}

function ProgressRow({
  label,
  value,
  total,
}) {
  const percentage = Math.min(
    100,
    Math.round(
      (value / total) * 100
    )
  );

  return (
    <div>
      <div className="flex items-center justify-between text-sm">
        <span className="text-slate-400">
          {label}
        </span>

        <span className="font-medium text-white">
          {value}
        </span>
      </div>

      <div className="mt-2 h-2 overflow-hidden rounded-full bg-slate-800">
        <div
          className="h-full rounded-full bg-blue-600 transition-all"
          style={{
            width: `${percentage}%`,
          }}
        />
      </div>
    </div>
  );
}

export default AnalyticsDashboard;
