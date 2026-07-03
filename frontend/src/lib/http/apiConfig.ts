const defaultApiUrl = "http://127.0.0.1:8000";

export const apiConfig = {
  baseUrl: import.meta.env.VITE_API_URL ?? defaultApiUrl,
  token: import.meta.env.VITE_API_TOKEN,
};
