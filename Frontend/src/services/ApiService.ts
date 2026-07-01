import axios, { AxiosInstance, AxiosResponse } from 'axios';
import {
  AuthResponse,
  LoginRequest,
  RegisterRequest,
  Analyse,
  AnalysesResponse,
  FiltresHistorique,
  Maladie,
  StatsAdmin,
  PaginatedUsers,
  Utilisateur,
} from '../types';

const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

//  Instance Axios 
const api: AxiosInstance = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
});

// ── Intercepteur requête : injection JWT 
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ── Intercepteur réponse : gestion des 401 ───
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

//  AUTH
export const authService = {
  register: (data: RegisterRequest): Promise<AxiosResponse<AuthResponse>> =>
    api.post('/auth/register', data),

  login: (data: LoginRequest): Promise<AxiosResponse<AuthResponse>> =>
    api.post('/auth/login', data),

  logout: (): Promise<AxiosResponse<void>> =>
    api.post('/auth/logout'),

  me: (): Promise<AxiosResponse<Utilisateur>> =>
    api.get('/auth/me'),
};

//  DIAGNOSTIC
export const diagnoseService = {
  /**
   * Upload une image et déclenche l'analyse IA.
   * Retourne le résultat complet avec diagnostic et recommandations.
   */
  uploadAndAnalyse: (
    file: File,
    notes?: string
  ): Promise<AxiosResponse<Analyse>> => {
    const formData = new FormData();
    formData.append('image', file);
    if (notes) formData.append('notes', notes);
    return api.post('/diagnose', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 60000, // 60s pour l'inférence IA
    });
  },
};

// ═══════════════════════════════════════════════
//  ANALYSES (historique)
// ═══════════════════════════════════════════════
export const analysesService = {
  /** Liste paginée avec filtres */
  list: (filtres: FiltresHistorique): Promise<AxiosResponse<AnalysesResponse>> => {
    const params = new URLSearchParams();
    params.append('page', String(filtres.page));
    params.append('limit', String(filtres.limit));
    if (filtres.maladie)    params.append('maladie', filtres.maladie);
    if (filtres.gravite)    params.append('gravite', filtres.gravite);
    if (filtres.date_debut) params.append('date_debut', filtres.date_debut);
    if (filtres.date_fin)   params.append('date_fin', filtres.date_fin);
    return api.get(`/analyses?${params.toString()}`);
  },

  /** Détail d'une analyse */
  getById: (id: number): Promise<AxiosResponse<Analyse>> =>
    api.get(`/analyses/${id}`),

  /** Suppression */
  delete: (id: number): Promise<AxiosResponse<void>> =>
    api.delete(`/analyses/${id}`),

  /** Export PDF */
  exportPDF: (id: number): Promise<AxiosResponse<Blob>> =>
    api.get(`/analyses/${id}/export`, { responseType: 'blob' }),
};

// ═══════════════════════════════════════════════
//  MALADIES
// ═══════════════════════════════════════════════
export const maladiesService = {
  list: (): Promise<AxiosResponse<Maladie[]>> =>
    api.get('/maladies'),

  recommandations: (id: number): Promise<AxiosResponse<Maladie>> =>
    api.get(`/maladies/${id}/recommandations`),
};

// ═══════════════════════════════════════════════
//  ADMIN
// ═══════════════════════════════════════════════
export const adminService = {
  getUsers: (page = 1): Promise<AxiosResponse<PaginatedUsers>> =>
    api.get(`/admin/users?page=${page}`),

  updateUser: (id: number, data: Partial<Utilisateur>): Promise<AxiosResponse<Utilisateur>> =>
    api.put(`/admin/users/${id}`, data),

  deleteUser: (id: number): Promise<AxiosResponse<void>> =>
    api.delete(`/admin/users/${id}`),

  getStats: (): Promise<AxiosResponse<StatsAdmin>> =>
    api.get('/admin/stats'),

  deployModele: (file: File): Promise<AxiosResponse<void>> => {
    const formData = new FormData();
    formData.append('modele', file);
    return api.post('/admin/modele', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
};

export default api;