import {
  useEffect,
  useRef,
  useState,
} from "react";

import {
  BarChart3,
  Bot,
  Check,
  Clipboard,
  Files,
  Menu,
  Plus,
  Send,
  Trash2,
  Upload,
  User,
  X,
  Download,
  FileDown,
  LogOut,
} from "lucide-react";

import ReactMarkdown from "react-markdown";

import API, {
  loginUser,
  registerUser,
  sendMessage,
} from "./api/api";
import {
  exportChatAsMarkdown,
  exportChatAsText,
} from "./utils/exportChat";

import DocumentManager from "./components/DocumentManager";
import UploadDocument from "./components/UploadDocument";
import WelcomeDashboard from "./components/WelcomeDashboard";
import AnalyticsDashboard from "./components/AnalyticsDashboard";

const DEFAULT_MESSAGE = {
  role: "assistant",
  content:
    "Hello! I am your Enterprise AI Assistant. Ask me anything about your documents or enterprise knowledge base.",
  sources: [],
};

function App() {
  const [authenticated, setAuthenticated] =
    useState(() => Boolean(localStorage.getItem("enterprise_admin_token")));

  const [sidebarOpen, setSidebarOpen] =
    useState(true);

  const [uploadOpen, setUploadOpen] =
    useState(false);

  const [
    documentsOpen,
    setDocumentsOpen,
  ] = useState(false);

  const [analyticsOpen,
     setAnalyticsOpen
    ] = useState(false);

  const [
    exportMenuOpen,
    setExportMenuOpen,
  ] = useState(false);

  const [message, setMessage] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [
    backendOnline,
    setBackendOnline,
  ] = useState(false);

  const [
    copiedIndex,
    setCopiedIndex,
  ] = useState(null);

  const [
    notification,
    setNotification,
  ] = useState(null);

  const [messages, setMessages] =
    useState(() => {
      const savedMessages =
        localStorage.getItem(
          "enterprise-chat-history"
        );

      if (savedMessages) {
        try {
          const parsedMessages =
            JSON.parse(savedMessages);

          if (
            Array.isArray(parsedMessages) &&
            parsedMessages.length > 0
          ) {
            return parsedMessages;
          }
        } catch (error) {
          console.error(
            "Unable to load chat history:",
            error
          );
        }
      }

      return [DEFAULT_MESSAGE];
    });

  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  async function checkBackendHealth() {
    try {
      await API.get("/health");
      setBackendOnline(true);
    } catch {
      setBackendOnline(false);
    }
  }

  useEffect(() => {
    localStorage.setItem(
      "enterprise-chat-history",
      JSON.stringify(messages)
    );
  }, [messages]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  useEffect(() => {
    const initialCheck = window.setTimeout(() => {
      void checkBackendHealth();
    }, 0);

    const interval = setInterval(
      checkBackendHealth,
      10000
    );

    return () => {
      window.clearTimeout(initialCheck);
      clearInterval(interval);
    };
  }, []);

  useEffect(() => {
    if (!notification) {
      return undefined;
    }

    const timer = setTimeout(() => {
      setNotification(null);
    }, 3000);

    return () => {
      clearTimeout(timer);
    };
  }, [notification]);

  useEffect(() => {
    const textarea =
      textareaRef.current;

    if (!textarea) {
      return;
    }

    textarea.style.height = "auto";

    textarea.style.height = `${Math.min(
      textarea.scrollHeight,
      160
    )}px`;
  }, [message]);

  const showNotification = (
    notificationMessage,
    type = "success"
  ) => {
    setNotification({
      message: notificationMessage,
      type,
    });
  };

  const handleSend = async () => {
    const trimmedMessage =
      message.trim();

    if (!trimmedMessage || loading) {
      return;
    }

    const userMessage = {
      role: "user",
      content: trimmedMessage,
      sources: [],
    };

    setMessages(
      (previousMessages) => [
        ...previousMessages,
        userMessage,
      ]
    );

    setMessage("");
    setLoading(true);

    try {
      const data = await sendMessage(
        trimmedMessage
      );

      const assistantMessage = {
        role: "assistant",
        content:
          data.response ||
          data.answer ||
          "The backend returned an empty response.",
        sources: Array.isArray(
          data.sources
        )
          ? data.sources
          : [],
      };

      setMessages(
        (previousMessages) => [
          ...previousMessages,
          assistantMessage,
        ]
      );

      setBackendOnline(true);
    } catch (error) {
      console.error(
        "Chat request failed:",
        error
      );

      const backendMessage =
        error.response?.data?.detail ||
        error.response?.data?.message ||
        error.message;

      setMessages(
        (previousMessages) => [
          ...previousMessages,
          {
            role: "assistant",
            content:
              backendMessage ||
              "Unable to connect to the FastAPI backend. Make sure FastAPI, Ollama and Neo4j are running.",
            sources: [],
          },
        ]
      );

      showNotification(
        "Chat request failed.",
        "error"
      );

      setBackendOnline(false);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {
      event.preventDefault();
      handleSend();
    }
  };

  const startNewChat = () => {
    setMessages([DEFAULT_MESSAGE]);
    setMessage("");

    showNotification(
      "New chat started."
    );

    if (window.innerWidth < 768) {
      setSidebarOpen(false);
    }
  };

  const clearChatHistory = () => {
    setMessages([DEFAULT_MESSAGE]);

    localStorage.removeItem(
      "enterprise-chat-history"
    );

    showNotification(
      "Chat history cleared."
    );
  };

  const handleLogout = () => {
    localStorage.removeItem("enterprise_admin_token");
    setUploadOpen(false);
    setDocumentsOpen(false);
    setAnalyticsOpen(false);
    setExportMenuOpen(false);
    setAuthenticated(false);
  };

  const copyMessage = async (
    content,
    index
  ) => {
    try {
      await navigator.clipboard.writeText(
        content
      );

      setCopiedIndex(index);

      showNotification(
        "Message copied."
      );

      setTimeout(() => {
        setCopiedIndex(null);
      }, 1500);
    } catch (error) {
      console.error(
        "Copy failed:",
        error
      );

      showNotification(
        "Unable to copy message.",
        "error"
      );
    }
  };

  const getUniqueSources = (sources) => {
    if (!Array.isArray(sources)) {
      return [];
    }

    const uniqueSources = new Map();

    sources.forEach((source) => {
      const filename =
        source.filename ||
        source.source ||
        source.original_filename ||
        "Unknown document";

      const chunk =
        source.chunk ??
        source.chunk_index ??
        null;

      const key =
        `${filename}-${chunk}`;

      if (!uniqueSources.has(key)) {
        uniqueSources.set(key, {
          ...source,
          filename,
          chunk,
        });
      }
    });

    return Array.from(
      uniqueSources.values()
    );
  };

  const handlePromptSelect = (
    selectedPrompt
  ) => {
    setMessage(selectedPrompt);

    setTimeout(() => {
      textareaRef.current?.focus();
    }, 0);
  };

  const handleExportText = () => {
    if (messages.length === 0) {
      showNotification(
        "There is no chat to export.",
        "error"
      );

      return;
    }

    exportChatAsText(messages);

    setExportMenuOpen(false);

    showNotification(
      "Chat exported as TXT."
    );
  };

  const handleExportMarkdown = () => {
    if (messages.length === 0) {
      showNotification(
        "There is no chat to export.",
        "error"
      );

      return;
    }

    exportChatAsMarkdown(messages);

    setExportMenuOpen(false);

    showNotification(
      "Chat exported as Markdown."
    );
  };

  const showWelcomeDashboard =
    messages.length === 1 &&
    messages[0].role === "assistant" &&
    messages[0].content ===
      DEFAULT_MESSAGE.content;

  if (!authenticated) {
    return <Login onAuthenticated={() => setAuthenticated(true)} />;
  }

  return (
    <div className="flex h-screen overflow-hidden bg-slate-950 text-white">
      {notification && (
        <div
          className={`fixed right-4 top-4 max-w-sm rounded-xl border px-4 py-3 text-sm shadow-2xl ${
            notification.type ===
            "error"
              ? "border-red-500/40 bg-red-950 text-red-200"
              : "border-green-500/40 bg-green-950 text-green-200"
          }`}
          style={{ zIndex: 100 }}
        >
          {notification.message}
        </div>
      )}

      {uploadOpen && (
        <UploadDocument
          onClose={() =>
            setUploadOpen(false)
          }
          onUploadSuccess={(result) => {
            setUploadOpen(false);

            const chunksAdded =
              result?.chunks_added;

            const successMessage =
              chunksAdded !== undefined
                ? `Document uploaded successfully. ${chunksAdded} chunks indexed.`
                : "Document uploaded successfully.";

            showNotification(
              successMessage
            );
          }}
        />
      )}

      {documentsOpen && (
        <DocumentManager
          onClose={() =>
            setDocumentsOpen(false)
          }
        />
      )}
{analyticsOpen && (
  <AnalyticsDashboard
    onClose={() =>
      setAnalyticsOpen(false)
    }
    messages={messages}
    backendOnline={backendOnline}
  />
)}
      {sidebarOpen && (
        <>
          <div
            className="fixed inset-0 z-30 bg-black/60 md:hidden"
            onClick={() =>
              setSidebarOpen(false)
            }
            role="presentation"
          />

          <aside className="fixed inset-y-0 left-0 z-40 flex w-72 flex-col border-r border-slate-800 bg-slate-900 md:static md:z-auto">
            <div className="border-b border-slate-800 p-5">
              <div className="flex items-center justify-between">
                <div>
                  <h1 className="text-xl font-bold">
                    Enterprise AI
                  </h1>

                  <p className="mt-1 text-sm text-slate-400">
                    Intelligent Assistant
                  </p>
                </div>

                <button
                  type="button"
                  onClick={() =>
                    setSidebarOpen(false)
                  }
                  className="rounded-lg p-2 text-slate-400 transition hover:bg-slate-800 hover:text-white md:hidden"
                  aria-label="Close sidebar"
                >
                  <X size={20} />
                </button>
              </div>
            </div>

            <div className="space-y-3 p-4">
              <button
                type="button"
                onClick={startNewChat}
                className="flex w-full items-center justify-center gap-2 rounded-xl bg-blue-600 px-4 py-3 font-medium transition hover:bg-blue-500"
              >
                <Plus size={19} />
                New Chat
              </button>

              <button
                type="button"
                onClick={clearChatHistory}
                className="flex w-full items-center justify-center gap-2 rounded-xl border border-slate-700 px-4 py-3 font-medium text-slate-300 transition hover:bg-slate-800"
              >
                <Trash2 size={18} />
                Clear History
              </button>

              <button
                type="button"
                onClick={handleLogout}
                className="flex w-full items-center justify-center gap-2 rounded-xl border border-red-500/40 px-4 py-3 font-medium text-red-300 transition hover:bg-red-500/10 hover:text-red-200"
              >
                <LogOut size={18} />
                Log out
              </button>

              <button
                type="button"
                onClick={() => {
                  setUploadOpen(true);

                  if (
                    window.innerWidth <
                    768
                  ) {
                    setSidebarOpen(false);
                  }
                }}
                className="flex w-full items-center justify-center gap-2 rounded-xl border border-slate-700 px-4 py-3 font-medium text-slate-300 transition hover:border-blue-500 hover:bg-slate-800 hover:text-white"
              >
                <Upload size={18} />
                Upload PDF
              </button>

              <button
                type="button"
                onClick={() => {
                  setDocumentsOpen(true);

                  if (
                    window.innerWidth <
                    768
                  ) {
                    setSidebarOpen(false);
                  }
                }}
                className="flex w-full items-center justify-center gap-2 rounded-xl border border-slate-700 px-4 py-3 font-medium text-slate-300 transition hover:border-blue-500 hover:bg-slate-800 hover:text-white"
              >
                <Files size={18} />
                Documents
              </button>

              <button
                type="button"
                onClick={() => {
                  setAnalyticsOpen(true);

                  if (window.innerWidth < 768) {
                    setSidebarOpen(false);
                  }
                }}
                className="flex w-full items-center justify-center gap-2 rounded-xl border border-slate-700 px-4 py-3 font-medium text-slate-300 transition hover:border-blue-500 hover:bg-slate-800 hover:text-white"
              >
                <BarChart3 size={18} />
                Analytics
              </button>

              <div className="relative">
                <button
                  type="button"
                  onClick={() =>
                    setExportMenuOpen(
                      (previousValue) =>
                        !previousValue
                    )
                  }
                  className="flex w-full items-center justify-center gap-2 rounded-xl border border-slate-700 px-4 py-3 font-medium text-slate-300 transition hover:border-blue-500 hover:bg-slate-800 hover:text-white"
                >
                  <Download size={18} />
                  Export Chat
                </button>

                {exportMenuOpen && (
                  <div className="mt-2 overflow-hidden rounded-xl border border-slate-700 bg-slate-950 shadow-xl">
                    <button
                      type="button"
                      onClick={handleExportText}
                      className="flex w-full items-center gap-3 px-4 py-3 text-left text-sm text-slate-300 transition hover:bg-slate-800 hover:text-white"
                    >
                      <FileDown size={17} />
                      Export as TXT
                    </button>

                    <button
                      type="button"
                      onClick={handleExportMarkdown}
                      className="flex w-full items-center gap-3 border-t border-slate-800 px-4 py-3 text-left text-sm text-slate-300 transition hover:bg-slate-800 hover:text-white"
                    >
                      <FileDown size={17} />
                      Export as Markdown
                    </button>
                  </div>
                )}
              </div>
            </div>

            <div className="flex-1 overflow-y-auto px-4">
              <p className="mb-3 text-xs font-semibold uppercase tracking-wider text-slate-500">
                AI Features
              </p>

              <div className="space-y-2 text-sm">
                <FeatureItem
                  name="Hybrid RAG"
                  active
                />

                <FeatureItem name="GraphRAG" />
                <FeatureItem name="LlamaIndex" />
                <FeatureItem name="LangGraph" />
                <FeatureItem name="MCP Tools" />
                <FeatureItem name="Conversation Memory" />
              </div>
            </div>

            <div className="border-t border-slate-800 p-4">
              <div className="rounded-xl bg-slate-800 p-4">
                <div className="flex items-center gap-2 text-sm">
                  <span
                    className={`h-2.5 w-2.5 rounded-full ${
                      backendOnline
                        ? "bg-green-500"
                        : "bg-red-500"
                    }`}
                  />

                  {backendOnline
                    ? "Backend connected"
                    : "Backend offline"}
                </div>

                <p className="mt-2 text-xs text-slate-400">
                  Model: llama3.2
                </p>
              </div>
            </div>
          </aside>
        </>
      )}

      <main className="flex min-w-0 flex-1 flex-col">
        <header className="flex h-16 shrink-0 items-center justify-between border-b border-slate-800 bg-slate-900 px-4 md:px-6">
          <div className="flex min-w-0 items-center gap-3">
            <button
              type="button"
              onClick={() =>
                setSidebarOpen(
                  (previousValue) =>
                    !previousValue
                )
              }
              className="rounded-lg p-2 transition hover:bg-slate-800"
              aria-label="Toggle sidebar"
            >
              <Menu size={21} />
            </button>

            <div className="min-w-0">
              <h2 className="truncate font-semibold">
                Enterprise AI Assistant
              </h2>

              <p className="hidden truncate text-xs text-slate-400 sm:block">
                RAG · GraphRAG · LangGraph · MCP
              </p>
            </div>
          </div>

          <div
            className={`flex shrink-0 items-center gap-2 text-sm ${
              backendOnline
                ? "text-green-400"
                : "text-red-400"
            }`}
          >
            <span
              className={`h-2.5 w-2.5 rounded-full ${
                backendOnline
                  ? "bg-green-500"
                  : "bg-red-500"
              }`}
            />

            <span className="hidden sm:inline">
              {backendOnline
                ? "Online"
                : "Offline"}
            </span>
          </div>
        </header>

        <section className="flex-1 overflow-y-auto px-4 py-6">
          {showWelcomeDashboard ? (
            <WelcomeDashboard
              backendOnline={
                backendOnline
              }
              onPromptSelect={
                handlePromptSelect
              }
            />
          ) : (
            <div className="mx-auto max-w-4xl space-y-6">
              {messages.map(
                (
                  currentMessage,
                  index
                ) => {
                  const uniqueSources =
                    getUniqueSources(
                      currentMessage.sources
                    );

                  return (
                    <div
                      key={`${currentMessage.role}-${index}`}
                      className={`flex gap-3 ${
                        currentMessage.role ===
                        "user"
                          ? "justify-end"
                          : "justify-start"
                      }`}
                    >
                      {currentMessage.role ===
                        "assistant" && (
                        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-blue-600">
                          <Bot size={20} />
                        </div>
                      )}

                      <div
                        className={`group relative max-w-[85%] rounded-2xl px-5 py-4 ${
                          currentMessage.role ===
                          "user"
                            ? "bg-blue-600 text-white"
                            : "border border-slate-800 bg-slate-900 text-slate-200"
                        }`}
                      >
                        <div className="max-w-none wrap-break-word text-sm leading-7 text-slate-200 [&_a]:text-blue-400 [&_a]:underline [&_code]:rounded [&_code]:bg-slate-800 [&_code]:px-1 [&_pre]:overflow-x-auto [&_pre]:rounded [&_pre]:bg-slate-950 [&_pre]:p-3">
                          <ReactMarkdown>
                            {
                              currentMessage.content
                            }
                          </ReactMarkdown>
                        </div>

                        {currentMessage.role ===
                          "assistant" &&
                          uniqueSources.length >
                            0 && (
                            <div className="mt-4 border-t border-slate-700 pt-3">
                              <p className="mb-2 flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-slate-400">
                                <Files
                                  size={14}
                                />
                                Sources
                              </p>

                              <div className="flex flex-wrap gap-2">
                                {uniqueSources.map(
                                  (
                                    source,
                                    sourceIndex
                                  ) => (
                                    <div
                                      key={`${source.filename}-${source.chunk}-${sourceIndex}`}
                                      className="flex max-w-full items-center gap-2 rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-xs text-slate-300"
                                    >
                                      <Files
                                        size={
                                          14
                                        }
                                        className="shrink-0 text-blue-400"
                                      />

                                      <span className="max-w-48 truncate sm:max-w-64">
                                        {
                                          source.filename
                                        }
                                      </span>

                                      {source.chunk !==
                                        null &&
                                        source.chunk !==
                                          undefined && (
                                          <span className="shrink-0 rounded bg-slate-700 px-1.5 py-0.5 text-[10px] text-slate-400">
                                            Chunk{" "}
                                            {
                                              source.chunk
                                            }
                                          </span>
                                        )}
                                    </div>
                                  )
                                )}
                              </div>
                            </div>
                          )}

                        {currentMessage.role ===
                          "assistant" && (
                          <button
                            type="button"
                            onClick={() =>
                              copyMessage(
                                currentMessage.content,
                                index
                              )
                            }
                            className="mt-3 flex items-center gap-1 rounded-md px-2 py-1 text-xs text-slate-400 transition hover:bg-slate-800 hover:text-white"
                          >
                            {copiedIndex ===
                            index ? (
                              <>
                                <Check
                                  size={
                                    14
                                  }
                                />
                                Copied
                              </>
                            ) : (
                              <>
                                <Clipboard
                                  size={
                                    14
                                  }
                                />
                                Copy
                              </>
                            )}
                          </button>
                        )}
                      </div>

                      {currentMessage.role ===
                        "user" && (
                        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-slate-700">
                          <User size={20} />
                        </div>
                      )}
                    </div>
                  );
                }
              )}

              {loading && (
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-600">
                    <Bot size={20} />
                  </div>

                  <div className="rounded-2xl border border-slate-800 bg-slate-900 px-5 py-4">
                    <div className="flex gap-1">
                      <span className="h-2 w-2 animate-bounce rounded-full bg-slate-400" />

                      <span className="h-2 w-2 animate-bounce rounded-full bg-slate-400 [animation-delay:150ms]" />

                      <span className="h-2 w-2 animate-bounce rounded-full bg-slate-400 [animation-delay:300ms]" />
                    </div>
                  </div>
                </div>
              )}

              <div
                ref={messagesEndRef}
              />
            </div>
          )}
        </section>

        <footer className="shrink-0 border-t border-slate-800 bg-slate-950 p-4">
          <div className="mx-auto max-w-4xl">
            <div className="flex items-end gap-3 rounded-2xl border border-slate-700 bg-slate-900 p-3 focus-within:border-blue-500">
              <textarea
                ref={textareaRef}
                value={message}
                onChange={(event) =>
                  setMessage(
                    event.target.value
                  )
                }
                onKeyDown={
                  handleKeyDown
                }
                placeholder="Ask your enterprise assistant..."
                rows={1}
                disabled={loading}
                className="max-h-40 min-h-11 flex-1 resize-none overflow-y-auto bg-transparent px-3 py-2 text-sm text-white outline-none placeholder:text-slate-500 disabled:opacity-60"
              />

              <button
                type="button"
                onClick={handleSend}
                disabled={
                  loading ||
                  !message.trim()
                }
                className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-blue-600 transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
                aria-label="Send message"
              >
                <Send size={19} />
              </button>
            </div>

            <p className="mt-2 text-center text-xs text-slate-500">
              Enter to send · Shift +
              Enter for new line
            </p>
          </div>
        </footer>
      </main>
    </div>
  );
}

function Login({ onAuthenticated }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [registering, setRegistering] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError("");

    try {
      if (registering) {
        await registerUser(username, password);
      }

      const data = await loginUser(username, password);
      localStorage.setItem("enterprise_admin_token", data.access_token);
      onAuthenticated();
    } catch (requestError) {
      setError(requestError.response?.data?.detail || "Unable to sign in.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-950 p-4 text-white">
      <form onSubmit={handleSubmit} className="w-full max-w-sm rounded-2xl border border-slate-700 bg-slate-900 p-6 shadow-2xl">
        <h1 className="text-xl font-semibold">{registering ? "Create account" : "Sign in"}</h1>
        <p className="mt-2 text-sm text-slate-400">Access the Enterprise AI Chatbot.</p>
        <label className="mt-5 block text-sm">Username<input value={username} onChange={(event) => setUsername(event.target.value)} className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2" required /></label>
        <label className="mt-4 block text-sm">Password<input type="password" value={password} onChange={(event) => setPassword(event.target.value)} className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2" required /></label>
        {error && <p className="mt-4 text-sm text-red-400">{error}</p>}
        <button type="submit" disabled={loading} className="mt-5 w-full rounded-lg bg-blue-600 px-4 py-2 font-medium hover:bg-blue-500 disabled:opacity-50">{loading ? "Please wait..." : registering ? "Create account" : "Sign in"}</button>
        <button type="button" onClick={() => { setRegistering((value) => !value); setError(""); }} className="mt-3 w-full text-sm text-blue-400 hover:text-blue-300">{registering ? "Already have an account? Sign in" : "Need an account? Register"}</button>
      </form>
    </main>
  );
}

function FeatureItem({
  name,
  active = false,
}) {
  return (
    <div
      className={`rounded-lg px-4 py-3 ${
        active
          ? "bg-slate-800 text-white"
          : "text-slate-400"
      }`}
    >
      {name}
    </div>
  );
}

export default App;
