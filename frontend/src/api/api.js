import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000",
  timeout: 120000,
  headers: {
    Accept: "application/json",
  },
});

API.interceptors.request.use((config) => {
  const token = localStorage.getItem("enterprise_admin_token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

API.interceptors.response.use(
  (response) => response,
  (error) => {
    const backendMessage =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      "Unable to connect to the backend.";

    console.error("API Error:", backendMessage);

    return Promise.reject(error);
  }
);

export const sendMessage = async (message) => {
  const response = await API.post("/chat", {
    message,
  });

  return response.data;
};

export const loginUser = async (username, password) => {
  const response = await API.post("/auth/login", { username, password });
  return response.data;
};

export const registerUser = async (username, password) => {
  const response = await API.post("/auth/register", { username, password });
  return response.data;
};

export const uploadDocument = async (
  file,
  onUploadProgress
) => {
  if (!file) {
    throw new Error("Please select a PDF file.");
  }

  if (file.type !== "application/pdf") {
    throw new Error("Only PDF files are allowed.");
  }

  const formData = new FormData();

  formData.append("file", file);

  const response = await API.post(
    "/upload",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
      onUploadProgress,
    }
  );

  return response.data;
};

export const getDocuments = async () => {
  const response = await API.get("/documents");

  return response.data;
};

export const deleteDocument = async (
  filename
) => {
  if (!filename) {
    throw new Error("Filename is required.");
  }

  const encodedFilename =
    encodeURIComponent(filename);

  const response = await API.delete(
    `/documents/${encodedFilename}`
  );

  return response.data;
};

export const checkBackendHealth = async () => {
  const response = await API.get("/health");

  return response.data;
};

export default API;
