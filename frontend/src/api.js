import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json"
  }
});

export async function getRecommendations(payload) {
  const response = await api.post(
    "/api/recommendations",
    payload
  );

  return response.data;
}

export default api;