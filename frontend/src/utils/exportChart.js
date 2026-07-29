const getTimestamp = () => {
  return new Date().toLocaleString();
};

const buildTextContent = (messages) => {
  const header = [
    "Enterprise AI Assistant",
    `Exported: ${getTimestamp()}`,
    "",
    "----------------------------------------",
    "",
  ].join("\n");

  const conversation = messages
    .map((message) => {
      const role =
        message.role === "user"
          ? "USER"
          : "ASSISTANT";

      let content = `${role}\n${message.content}`;

      if (
        Array.isArray(message.sources) &&
        message.sources.length > 0
      ) {
        const sources = message.sources
          .map((source, index) => {
            const filename =
              source.filename ||
              source.source ||
              source.original_filename ||
              "Unknown document";

            const chunk =
              source.chunk ??
              source.chunk_index;

            return `${index + 1}. ${filename}${
              chunk !== null &&
              chunk !== undefined
                ? ` - Chunk ${chunk}`
                : ""
            }`;
          })
          .join("\n");

        content += `\n\nSources:\n${sources}`;
      }

      return content;
    })
    .join(
      "\n\n----------------------------------------\n\n"
    );

  return header + conversation;
};

const buildMarkdownContent = (
  messages
) => {
  const header = [
    "# Enterprise AI Assistant",
    "",
    `**Exported:** ${getTimestamp()}`,
    "",
    "---",
    "",
  ].join("\n");

  const conversation = messages
    .map((message) => {
      const role =
        message.role === "user"
          ? "User"
          : "Assistant";

      let content = `## ${role}\n\n${message.content}`;

      if (
        Array.isArray(message.sources) &&
        message.sources.length > 0
      ) {
        const sources = message.sources
          .map((source) => {
            const filename =
              source.filename ||
              source.source ||
              source.original_filename ||
              "Unknown document";

            const chunk =
              source.chunk ??
              source.chunk_index;

            return `- ${filename}${
              chunk !== null &&
              chunk !== undefined
                ? ` — Chunk ${chunk}`
                : ""
            }`;
          })
          .join("\n");

        content += `\n\n### Sources\n\n${sources}`;
      }

      return content;
    })
    .join("\n\n---\n\n");

  return header + conversation;
};

const downloadFile = (
  content,
  filename,
  mimeType
) => {
  const blob = new Blob([content], {
    type: mimeType,
  });

  const url =
    URL.createObjectURL(blob);

  const link =
    document.createElement("a");

  link.href = url;
  link.download = filename;

  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);

  URL.revokeObjectURL(url);
};

export const exportChatAsText = (
  messages
) => {
  const content =
    buildTextContent(messages);

  downloadFile(
    content,
    "enterprise-ai-chat.txt",
    "text/plain;charset=utf-8"
  );
};

export const exportChatAsMarkdown = (
  messages
) => {
  const content =
    buildMarkdownContent(messages);

  downloadFile(
    content,
    "enterprise-ai-chat.md",
    "text/markdown;charset=utf-8"
  );
};