import React, { useMemo } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ArrowLeft, Leaf, ShieldCheck, Sparkles } from 'lucide-react';
import { Layout } from '../components';

const sampleAnalyses = [
  {
    id: 1,
    date: '2026-07-01T09:30:00',
    maladie: 'Rouille noire',
    gravite: 'Élevée',
    confiance: '94 %',
    description: 'Les lésions sont typiques d’une infection fongique avancée sur les feuilles du cacaoyer.',
    recommandations: ['Éliminer les feuilles affectées', 'Appliquer un traitement fongicide adapté', 'Surveiller l’humidité ambiante'],
  },
  {
    id: 2,
    date: '2026-06-28T16:15:00',
    maladie: null,
    gravite: 'Saine',
    confiance: '97 %',
    description: 'Aucune signature pathologique n’a été détectée sur cette image. La plante semble en bonne santé.',
    recommandations: ['Continuer la surveillance', 'Maintenir un bon entretien', 'Préserver l’équilibre nutritionnel'],
  },
];

const AnalyseDetailPage: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const analyse = useMemo(() => {
    const parsedId = Number(id);
    return sampleAnalyses.find((item) => item.id === parsedId) ?? null;
  }, [id]);

  if (!analyse) {
    return (
      <Layout>
        <div className="card mx-auto max-w-2xl text-center">
          <p className="text-sm font-semibold uppercase tracking-[0.25em] text-stone-500">Analyse introuvable</p>
          <h1 className="mt-3 text-2xl font-semibold text-stone-900">Cette analyse n’existe pas ou a été supprimée.</h1>
          <button className="btn-primary mt-6" onClick={() => navigate('/historique')}>
            Retour à l’historique
          </button>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="mx-auto max-w-4xl space-y-6">
        <button className="btn-secondary" onClick={() => navigate('/historique')}>
          <ArrowLeft size={16} className="mr-2" />
          Retour à l’historique
        </button>

        <div className="rounded-[2rem] border border-stone-200/80 bg-white/90 p-8 shadow-premium">
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.25em] text-stone-500">Rapport détaillé</p>
              <h1 className="mt-2 text-3xl font-semibold text-stone-900">
                {analyse.maladie ?? 'Plante saine'}
              </h1>
              <p className="mt-2 text-sm text-stone-600">Analyse enregistrée le {analyse.date}</p>
            </div>
            <div className="rounded-2xl bg-emerald-50 p-4 text-emerald-700">
              <ShieldCheck size={24} />
            </div>
          </div>

          <div className="mt-8 grid gap-4 lg:grid-cols-[1.2fr_0.8fr]">
            <div className="card">
              <div className="flex items-center gap-2 text-lg font-semibold text-stone-900">
                <Sparkles size={18} className="text-amber-600" />
                Résumé du diagnostic
              </div>
              <p className="mt-4 text-sm leading-7 text-stone-600">{analyse.description}</p>
            </div>
            <div className="card space-y-4">
              <div>
                <p className="text-sm text-stone-500">Gravité</p>
                <p className="font-semibold text-stone-900">{analyse.gravite}</p>
              </div>
              <div>
                <p className="text-sm text-stone-500">Confiance</p>
                <p className="font-semibold text-stone-900">{analyse.confiance}</p>
              </div>
              <div>
                <p className="text-sm text-stone-500">Recommandations</p>
                <ul className="mt-2 space-y-2 text-sm text-stone-600">
                  {analyse.recommandations.map((item) => (
                    <li key={item} className="flex items-start gap-2">
                      <Leaf size={14} className="mt-1 text-emerald-600" />
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default AnalyseDetailPage;
