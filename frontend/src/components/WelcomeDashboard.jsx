import {
  BarChart3,
  BrainCircuit,
  FileSearch,
  Network,
  Sparkles,
} from "lucide-react";

const quickPrompts = [
  {
    title: "Summarise documents",
    description:
      "Get a concise summary of uploaded PDFs.",
    prompt:
      "Summarise the important information from the uploaded documents.",
    icon: FileSearch,
  },
  {
    title: "Compare information",
    description:
      "Compare concepts found across documents.",
    prompt:
      "Compare the key concepts from my uploaded documents.",
    icon: BarChart3,
  },
  {
    title: "Explore relationships",
    description:
      "Use GraphRAG to identify connected entities.",
    prompt:
      "Explain the important relationships between entities in the knowledge base.",
    icon: Network,
  },
  {
    title: "Ask an enterprise question",
    description:
      "Use hybrid retrieval for a detailed answer.",
    prompt:
      "What are the main insights available in the enterprise knowledge base?",
    icon: BrainCircuit,
  },
];

function WelcomeDashboard({
  onPromptSelect,
  backendOnline,
}) {
  return (
    <div className="mx-auto flex min-h-full max-w-5xl flex-col justify-center py-8">
      <div className="text-center">
        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-blue-600 shadow-lg shadow-blue-600/20">
          <Sparkles size={30} />
        </div>

        <h1 className="mt-6 text-3xl font-bold tracking-tight text-white sm:text-4xl">
          Enterprise AI Assistant
        </h1>

        <p className="mx-auto mt-3 max-w-2xl text-sm leading-6 text-slate-400 sm:text-base">
          Ask questions about your uploaded
          documents using Hybrid RAG,
          GraphRAG, LangGraph, LlamaIndex
          and MCP tools.
        </p>

        <div
          className={`mx-auto mt-4 inline-flex items-center gap-2 rounded-full border px-3 py-1.5 text-xs ${
            backendOnline
              ? "border-green-500/30 bg-green-500/10 text-green-400"
              : "border-red-500/30 bg-red-500/10 text-red-400"
          }`}
        >
          <span
            className={`h-2 w-2 rounded-full ${
              backendOnline
                ? "bg-green-500"
                : "bg-red-500"
            }`}
          />

          {backendOnline
            ? "Backend connected"
            : "Backend offline"}
        </div>
      </div>

      <div className="mt-10 grid gap-4 sm:grid-cols-2">
        {quickPrompts.map((item) => {
          const Icon = item.icon;

          return (
            <button
              key={item.title}
              type="button"
              onClick={() =>
                onPromptSelect(item.prompt)
              }
              className="group rounded-2xl border border-slate-800 bg-slate-900 p-5 text-left transition hover:-translate-y-0.5 hover:border-blue-500 hover:bg-slate-800"
            >
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-500/10 text-blue-400 transition group-hover:bg-blue-600 group-hover:text-white">
                <Icon size={21} />
              </div>

              <h2 className="mt-4 font-semibold text-white">
                {item.title}
              </h2>

              <p className="mt-2 text-sm leading-6 text-slate-400">
                {item.description}
              </p>
            </button>
          );
        })}
      </div>

      <div className="mt-8 grid gap-3 sm:grid-cols-3">
        <StatusCard
          value="Hybrid"
          label="Retrieval mode"
        />

        <StatusCard
          value="Local"
          label="Ollama model"
        />

        <StatusCard
          value="Secure"
          label="Knowledge base"
        />
      </div>
    </div>
  );
}

function StatusCard({ value, label }) {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 px-4 py-3 text-center">
      <p className="font-semibold text-white">
        {value}
      </p>

      <p className="mt-1 text-xs text-slate-500">
        {label}
      </p>
    </div>
  );
}

export default WelcomeDashboard;