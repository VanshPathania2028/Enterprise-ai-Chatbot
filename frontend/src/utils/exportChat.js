const downloadFile = (content, filename, type) => {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");

  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
};

const getExportDate = () =>
  new Date().toISOString().replace(/[:.]/g, "-");

const messageContent = (message) =>
  String(message?.content || "").trim();

export const exportChatAsText = (messages) => {
  const content = messages
    .map((message) => {
      const role = message?.role === "user" ? "You" : "Assistant";
      return `${role}:\n${messageContent(message)}`;
    })
    .join("\n\n");

  downloadFile(
    `${content}\n`,
    `enterprise-chat-${getExportDate()}.txt`,
    "text/plain;charset=utf-8",
  );
};

export const exportChatAsMarkdown = (messages) => {
  const content = messages
    .map((message) => {
      const role = message?.role === "user" ? "You" : "Assistant";
      return `## ${role}\n\n${messageContent(message)}`;
    })
    .join("\n\n---\n\n");

  downloadFile(
    `# Enterprise AI Chat Export\n\n${content}\n`,
    `enterprise-chat-${getExportDate()}.md`,
    "text/markdown;charset=utf-8",
  );
};
