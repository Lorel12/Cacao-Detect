export type Role = 'agriculteur' | 'agronome' | 'chercheur' | 'administrateur';
export type Gravite = 'faible' | 'modere' | 'eleve';
export type StatutAnalyse = 'en_cours' | 'termine' | 'erreur';

// ── Authentification 
export interface Utilisateur {
  id_utilisateur: number;
  nom: string;
  prenom: string;
  email: string;
  role: Role;
  statut: boolean;
  date_inscription: string;
  dernier_login?: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  nom: string;
  prenom: string;
  email: string;
  password: string;
  role: Role;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: Utilisateur;
}

// ── Maladie & Recommandation 
export interface Recommandation {
  id_recommandation: number;
  traitement: string;
  produit: string;
  dosage: string;
  frequence: string;
  source?: string;
}

export interface Maladie {
  id_maladie: number;
  nom_maladie: string;
  agent_causal: string;
  organes_touches: string;
  description: string;
  recommandations: Recommandation[];
}

// ── Diagnostic 
export interface Diagnostic {
  id_diagnostic: number;
  maladie: Maladie | null;
  niveau_gravite: Gravite | null;
  score_confiance: number;
  bbox: number[] | null;
  chemin_image_annotee: string | null;
  flag_avertissement: boolean;
}

// ── Analyse 
export interface Analyse {
  id_analyse: number;
  date_heure: string;
  statut: StatutAnalyse;
  duree_traitement_s: number | null;
  flag_avertissement: boolean;
  diagnostic: Diagnostic | null;
}

export interface AnalyseListItem {
  id_analyse: number;
  date_heure: string;
  statut: StatutAnalyse;
  maladie_nom: string | null;
  niveau_gravite: Gravite | null;
  score_confiance: number | null;
  image_annotee_url: string | null;
}

export interface AnalysesResponse {
  analyses: AnalyseListItem[];
  total: number;
  page: number;
  limit: number;
}

// ── Filtres 
export interface FiltresHistorique {
  maladie?: string;
  gravite?: Gravite | '';
  date_debut?: string;
  date_fin?: string;
  page: number;
  limit: number;
}

// ── Admin 
export interface StatsAdmin {
  total_utilisateurs: number;
  total_analyses: number;
  analyses_aujourd_hui: number;
  taux_detection: number;
  maladie_plus_frequente: string;
}

export interface PaginatedUsers {
  users: Utilisateur[];
  total: number;
  page: number;
}