import React, { useState, useRef, useCallback } from 'react';
import { toast } from 'react-toastify';
import {
  Upload, X, Loader2, CheckCircle, AlertTriangle,
  Leaf, Zap, Info, ChevronDown, ChevronUp,
} from 'lucide-react';
import { diagnoseService } from '../services/ApiService';
import { Analyse } from '../types';
import { GraviteBadge, Layout } from '../components';
import { validateImageFile, formatConfiance, formatDuree } from '../utils';

// ── Composant résultat 
const ResultatDiagnostic: React.FC<{ analyse: Analyse }> = ({ analyse }) => {
  const [showReco, setShowReco] = useState(true);
  const diag     = analyse.diagnostic;
  const estSain  = !diag?.maladie;

  return (
    <div className="space-y-4 animate-in fade-in duration-500">
      {/* Bandeau statut */}
      <div
        className={`rounded-xl p-4 flex items-center gap-3 border
          ${estSain
            ? 'bg-green-50 border-green-200'
            : diag?.niveau_gravite === 'eleve'
              ? 'bg-red-50 border-red-200'
              : 'bg-orange-50 border-orange-200'}`}
      >
        {estSain
          ? <CheckCircle className="text-green-500 shrink-0" size={24} />
          : <AlertTriangle className="text-orange-500 shrink-0" size={24} />}
        <div>
          <p className="font-semibold text-gray-900">
            {estSain ? 'Plante saine' : diag?.maladie?.nom_maladie}
          </p>
          <p className="text-sm text-gray-600">
            {estSain
              ? 'Aucune maladie détectée sur cette image.'
              : `Agent causal : ${diag?.maladie?.agent_causal}`}
          </p>
        </div>
      </div>

      {/* Avertissement confiance faible */}
      {analyse.flag_avertissement && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3
                        flex items-start gap-2 text-sm text-yellow-800">
          <Info size={16} className="shrink-0 mt-0.5" />
          Score de confiance faible (&lt; 60 %). Le résultat est indicatif.
          Consultez un expert agronome pour confirmation.
        </div>
      )}

      <div className="grid md:grid-cols-2 gap-4">
        {/* Informations diagnostic */}
        <div className="card space-y-3">
          <h3 className="font-semibold text-gray-900 flex items-center gap-2">
            <Zap size={16} className="text-primary-500" />
            Résultats de l'analyse
          </h3>
          <dl className="space-y-2 text-sm">
            <div className="flex justify-between">
              <dt className="text-gray-500">Maladie</dt>
              <dd className="font-medium">{diag?.maladie?.nom_maladie ?? '—'}</dd>
            </div>
            <div className="flex justify-between items-center">
              <dt className="text-gray-500">Niveau de gravité</dt>
              <dd><GraviteBadge gravite={diag?.niveau_gravite} /></dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-gray-500">Confiance</dt>
              <dd className="font-medium">{formatConfiance(diag?.score_confiance)}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-gray-500">Durée d'analyse</dt>
              <dd className="font-medium">{formatDuree(analyse.duree_traitement_s)}</dd>
            </div>
            {diag?.maladie?.organes_touches && (
              <div className="flex justify-between">
                <dt className="text-gray-500">Organes touchés</dt>
                <dd className="font-medium text-right">{diag.maladie.organes_touches}</dd>
              </div>
            )}
          </dl>
        </div>

        {/* Image annotée */}
        {diag?.chemin_image_annotee && (
          <div className="card p-0 overflow-hidden">
            <p className="text-xs text-gray-500 px-4 pt-3 pb-2 font-medium">
              Image annotée
            </p>
            <img
              src={diag.chemin_image_annotee}
              alt="Analyse annotée du modèle IA"
              className="w-full h-48 object-cover"
            />
          </div>
        )}
      </div>

      {/* Recommandations */}
      {!estSain && diag?.maladie?.recommandations &&
        diag.maladie.recommandations.length > 0 && (
        <div className="card">
          <button
            className="w-full flex items-center justify-between font-semibold
                       text-gray-900 text-sm"
            onClick={() => setShowReco(!showReco)}
          >
            <span className="flex items-center gap-2">
              <Leaf size={16} className="text-accent-500" />
              Recommandations de traitement
            </span>
            {showReco ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </button>

          {showReco && (
            <div className="mt-4 space-y-3">
              {diag.maladie.recommandations.map((reco) => (
                <div
                  key={reco.id_recommandation}
                  className="bg-green-50 border border-green-100 rounded-lg p-3 text-sm"
                >
                  <p className="font-semibold text-green-800">{reco.traitement}</p>
                  <div className="mt-1.5 grid grid-cols-2 gap-1 text-green-700">
                    <span><span className="font-medium">Produit :</span> {reco.produit}</span>
                    <span><span className="font-medium">Dosage :</span> {reco.dosage}</span>
                    <span className="col-span-2">
                      <span className="font-medium">Fréquence :</span> {reco.frequence}
                    </span>
                  </div>
                  {reco.source && (
                    <p className="text-xs text-green-600 mt-1">Source : {reco.source}</p>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Description maladie */}
      {diag?.maladie?.description && (
        <div className="card bg-blue-50 border-blue-100">
          <p className="text-sm font-medium text-blue-800 mb-1">
            À propos de la maladie
          </p>
          <p className="text-sm text-blue-700">{diag.maladie.description}</p>
        </div>
      )}
    </div>
  );
};

// ── Page principale 
const DiagnosticPage: React.FC = () => {
  const [file,      setFile]      = useState<File | null>(null);
  const [preview,   setPreview]   = useState<string | null>(null);
  const [notes,     setNotes]     = useState('');
  const [loading,   setLoading]   = useState(false);
  const [resultat,  setResultat]  = useState<Analyse | null>(null);
  const [dragging,  setDragging]  = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  // Sélection ou dépôt de fichier
  const handleFile = useCallback((f: File) => {
    const error = validateImageFile(f);
    if (error) { toast.error(error); return; }
    setFile(f);
    setResultat(null);
    const reader = new FileReader();
    reader.onload = (e) => setPreview(e.target?.result as string);
    reader.readAsDataURL(f);
  }, []);

  const onInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) handleFile(e.target.files[0]);
  };

  const onDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragging(false);
    if (e.dataTransfer.files?.[0]) handleFile(e.dataTransfer.files[0]);
  };

  const resetFile = () => {
    setFile(null);
    setPreview(null);
    setResultat(null);
    if (inputRef.current) inputRef.current.value = '';
  };

  // Envoi de l'analyse
  const handleAnalyse = async () => {
    if (!file) return;
    setLoading(true);
    setResultat(null);
    try {
      const response = await diagnoseService.uploadAndAnalyse(file, notes || undefined);
      setResultat(response.data);
      toast.success('Analyse terminée avec succès !');
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { detail?: string } } })
        ?.response?.data?.detail ?? "Erreur lors de l'analyse. Réessayez.";
      toast.error(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <div className="max-w-3xl mx-auto space-y-6">

        {/* Titre */}
        <div>
          <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <Leaf className="text-primary-500" />
            Diagnostic de plante
          </h1>
          <p className="text-gray-500 text-sm mt-1">
            Téléversez une photo de feuille ou de cabosse pour obtenir un diagnostic
            automatique en moins de 5 secondes.
          </p>
        </div>

        {/* Zone d'upload */}
        <div className="card">
          {!file ? (
            <div
              className={`border-2 border-dashed rounded-xl p-10 text-center cursor-pointer
                          transition-colors ${dragging
                            ? 'border-primary-400 bg-primary-50'
                            : 'border-gray-200 hover:border-primary-300 hover:bg-gray-50'}`}
              onClick={() => inputRef.current?.click()}
              onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
              onDragLeave={() => setDragging(false)}
              onDrop={onDrop}
            >
              <Upload size={36} className="mx-auto text-gray-300 mb-3" />
              <p className="font-semibold text-gray-700 mb-1">
                Glisser-déposer ou cliquer pour choisir
              </p>
              <p className="text-sm text-gray-400">JPEG, PNG — max 10 Mo</p>
              <button
                type="button"
                className="btn-secondary mt-4 text-sm"
                onClick={(e) => { e.stopPropagation(); inputRef.current?.click(); }}
              >
                Choisir un fichier
              </button>
              <input
                ref={inputRef}
                type="file"
                accept="image/jpeg,image/jpg,image/png"
                className="hidden"
                onChange={onInputChange}
              />
            </div>
          ) : (
            <div className="flex gap-4 items-start">
              {/* Prévisualisation */}
              <div className="relative shrink-0">
                <img
                  src={preview!}
                  alt="Aperçu de la feuille ou de la cabosse"
                  className="w-36 h-36 object-cover rounded-lg border border-gray-200"
                />
                <button
                  onClick={resetFile}
                  className="absolute -top-2 -right-2 bg-red-500 text-white
                             rounded-full w-6 h-6 flex items-center justify-center
                             hover:bg-red-600 shadow"
                >
                  <X size={12} />
                </button>
              </div>

              {/* Infos fichier + notes */}
              <div className="flex-1 space-y-3">
                <div>
                  <p className="font-medium text-gray-900 text-sm truncate">{file.name}</p>
                  <p className="text-xs text-gray-500">
                    {(file.size / 1024 / 1024).toFixed(2)} Mo · {file.type}
                  </p>
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-600 mb-1">
                    Notes (optionnel)
                  </label>
                  <textarea
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                    rows={2}
                    placeholder="Observations ou contexte supplémentaire..."
                    className="input-field text-sm resize-none"
                  />
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Bouton lancer */}
        {file && (
          <button
            onClick={handleAnalyse}
            disabled={loading}
            className="btn-primary w-full flex items-center justify-center gap-2 py-3 text-base"
          >
            {loading
              ? <><Loader2 size={18} className="animate-spin" /> Analyse en cours...</>
              : <><Zap size={18} /> Lancer l'analyse IA</>}
          </button>
        )}

        {/* Indicateur chargement */}
        {loading && (
          <div className="card text-center py-8 space-y-3">
            <div className="w-12 h-12 border-4 border-primary-200 border-t-primary-500
                            rounded-full animate-spin mx-auto" />
            <p className="text-gray-600 font-medium">Analyse IA en cours...</p>
            <p className="text-gray-400 text-sm">
              Le modèle YOLOv8 examine votre image. Cela peut prendre quelques secondes.
            </p>
          </div>
        )}

        {/* Résultats */}
        {resultat && !loading && (
          <ResultatDiagnostic analyse={resultat} />
        )}
      </div>
    </Layout>
  );
};

export default DiagnosticPage;