// ─────────────────────────────────────────────
//  utils/index.ts — Fonctions utilitaires
// ─────────────────────────────────────────────
import { Gravite, StatutAnalyse } from '../types';

/** Formate une date ISO en "15 mai 2026 à 10h23" */
export function formatDate(isoString: string): string {
  const date = new Date(isoString);
  return date.toLocaleDateString('fr-FR', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
  }) + ' à ' + date.toLocaleTimeString('fr-FR', {
    hour: '2-digit',
    minute: '2-digit',
  });
}

/** Formate une date en courte : "15/05/2026" */
export function formatDateCourte(isoString: string): string {
  const date = new Date(isoString);
  return date.toLocaleDateString('fr-FR');
}

/** Retourne le libellé français d'un niveau de gravité */
export function graviteLabel(g: Gravite | null | undefined): string {
  if (!g) return '—';
  const map: Record<Gravite, string> = {
    faible: 'Faible',
    modere: 'Modéré',
    eleve:  'Élevé',
  };
  return map[g];
}

/** Retourne la classe Tailwind CSS badge pour la gravité */
export function graviteBadgeClass(g: Gravite | null | undefined): string {
  if (!g) return 'badge-sain';
  const map: Record<Gravite, string> = {
    faible: 'badge-faible',
    modere: 'badge-modere',
    eleve:  'badge-eleve',
  };
  return map[g];
}

/** Retourne la couleur de fond pour un badge gravité */
export function graviteBgColor(g: Gravite | null | undefined): string {
  if (!g) return 'bg-green-50 text-green-700 border-green-200';
  const map: Record<Gravite, string> = {
    faible: 'bg-yellow-50 text-yellow-700 border-yellow-200',
    modere: 'bg-orange-50 text-orange-700 border-orange-200',
    eleve:  'bg-red-50 text-red-700 border-red-200',
  };
  return map[g];
}

/** Libellé du statut d'une analyse */
export function statutLabel(s: StatutAnalyse): string {
  const map: Record<StatutAnalyse, string> = {
    en_cours: 'En cours',
    termine:  'Terminé',
    erreur:   'Erreur',
  };
  return map[s];
}

/** Formate un score de confiance en pourcentage : 0.87 → "87 %" */
export function formatConfiance(score: number | null | undefined): string {
  if (score == null) return '—';
  return `${Math.round(score * 100)} %`;
}

/** Formate une durée en secondes : 3.456 → "3.5 s" */
export function formatDuree(s: number | null | undefined): string {
  if (s == null) return '—';
  return `${s.toFixed(1)} s`;
}

/** Valide qu'un fichier est une image acceptée (JPEG ou PNG, max 10 Mo) */
export function validateImageFile(file: File): string | null {
  const ACCEPTED = ['image/jpeg', 'image/jpg', 'image/png'];
  const MAX_MB   = 10;
  if (!ACCEPTED.includes(file.type)) {
    return 'Format non supporté. Utilisez un fichier JPEG ou PNG.';
  }
  if (file.size > MAX_MB * 1024 * 1024) {
    return `Fichier trop volumineux (max ${MAX_MB} Mo).`;
  }
  return null;
}

/** Télécharge un Blob en fichier */
export function downloadBlob(blob: Blob, filename: string): void {
  const url = window.URL.createObjectURL(blob);
  const a   = document.createElement('a');
  a.href     = url;
  a.download = filename;
  a.click();
  window.URL.revokeObjectURL(url);
}

/** Retourne le libellé de rôle en français */
export function roleLabel(role: string): string {
  const map: Record<string, string> = {
    agriculteur:    'Agriculteur',
    agronome:       'Agronome',
    chercheur:      'Chercheur',
    administrateur: 'Administrateur',
  };
  return map[role] ?? role;
}