import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Leaf, History, Zap, TrendingUp, Clock, AlertCircle } from 'lucide-react'
import { toast } from 'react-toastify'
import { Layout, GraviteBadge, EmptyState, StatCard, LoadingSpinner } from '../components'
import { analysesService } from '../services/ApiService'
import { AnalyseListItem } from '../types'
import { useAuth } from '../context/AuthContext'
import { formatDate, formatConfiance, statutLabel } from '../utils'

// ── Carte d'une analyse récente 
const AnalyseCard: React.FC<{ analyse: AnalyseListItem }> = ({ analyse }) => {
  const navigate = useNavigate()
  const estSain  = !analyse.maladie_nom

  return (
    <div
      className="card hover:shadow-md transition-shadow cursor-pointer border-l-4
                 flex items-start gap-4 p-4"
      style={{ borderLeftColor: estSain ? '#22c55e' :
               analyse.niveau_gravite === 'eleve'  ? '#ef4444' :
               analyse.niveau_gravite === 'modere' ? '#f97316' : '#eab308' }}
      onClick={() => navigate(`/historique/${analyse.id_analyse}`)}
    >
      {/* Miniature ou icône */}
      {analyse.image_annotee_url ? (
        <img
          src={analyse.image_annotee_url}
          alt="miniature"
          className="w-16 h-16 rounded-lg object-cover shrink-0 border border-gray-100"
        />
      ) : (
        <div className="w-16 h-16 rounded-lg bg-gray-100 flex items-center
                        justify-center shrink-0">
          <Leaf size={24} className="text-gray-300" />
        </div>
      )}

      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between gap-2 flex-wrap">
          <p className="font-semibold text-gray-900 text-sm truncate">
            {estSain ? 'Plante saine' : analyse.maladie_nom}
          </p>
          <GraviteBadge gravite={analyse.niveau_gravite} />
        </div>
        <p className="text-xs text-gray-400 mt-0.5">{formatDate(analyse.date_heure)}</p>
        <div className="flex items-center gap-3 mt-1.5">
          <span className={`text-xs px-2 py-0.5 rounded-full font-medium
            ${analyse.statut === 'termine' ? 'bg-green-50 text-green-700' :
              analyse.statut === 'erreur'  ? 'bg-red-50 text-red-700' :
                                             'bg-yellow-50 text-yellow-700'}`}>
            {statutLabel(analyse.statut)}
          </span>
          {analyse.score_confiance != null && (
            <span className="text-xs text-gray-400">
              Confiance : {formatConfiance(analyse.score_confiance)}
            </span>
          )}
        </div>
      </div>
    </div>
  )
}

// ── Page principale 
const DashboardPage: React.FC = () => {
  const { user }  = useAuth()
  const navigate  = useNavigate()
  const [analyses, setAnalyses] = useState<AnalyseListItem[]>([])
  const [loading,  setLoading]  = useState(true)

  // Stats calculées côté client sur les données récupérées
  const totalAnalyses   = analyses.length
  const analysesReussies = analyses.filter(a => a.statut === 'termine').length
  const maladiesDetect   = analyses.filter(a => a.maladie_nom).length
  const derniere         = analyses[0] ?? null

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await analysesService.list({ page: 1, limit: 5 })
        setAnalyses(res.data.analyses)
      } catch {
        toast.error('Impossible de charger le tableau de bord.')
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  if (loading) return <LoadingSpinner message="Chargement du tableau de bord..." />

  return (
    <Layout>
      <div className="space-y-8">

        {/* Salutation */}
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            Bonjour, {user?.prenom} 👋
          </h1>
          <p className="text-gray-500 text-sm mt-1">
            Voici un résumé de votre activité sur CacaoDetect.
          </p>
        </div>

        {/* Statistiques */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <StatCard
            label="Analyses effectuées"
            value={totalAnalyses}
            icon={<Zap size={22} />}
            color="text-primary-500"
          />
          <StatCard
            label="Analyses réussies"
            value={analysesReussies}
            icon={<TrendingUp size={22} />}
            color="text-green-500"
          />
          <StatCard
            label="Maladies détectées"
            value={maladiesDetect}
            icon={<AlertCircle size={22} />}
            color="text-red-500"
          />
          <StatCard
            label="Dernière analyse"
            value={derniere ? formatDate(derniere.date_heure).split(' à')[0] : '—'}
            icon={<Clock size={22} />}
            color="text-orange-500"
          />
        </div>

        {/* CTA Diagnostic */}
        <div className="bg-gradient-to-r from-primary-500 to-primary-600
                        rounded-2xl p-6 text-white flex items-center
                        justify-between flex-wrap gap-4">
          <div>
            <h2 className="text-xl font-bold">Lancer un nouveau diagnostic</h2>
            <p className="text-white/80 text-sm mt-1">
              Téléversez une photo de feuille ou de cabosse pour obtenir
              un diagnostic en quelques secondes.
            </p>
          </div>
          <button
            className="bg-white text-primary-600 font-semibold px-5 py-2.5
                       rounded-lg hover:bg-white/90 transition-colors shrink-0
                       flex items-center gap-2"
            onClick={() => navigate('/diagnostic')}
          >
            <Leaf size={16} />
            Analyser une image
          </button>
        </div>

        {/* Analyses récentes */}
        <div>
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold text-gray-900 flex items-center gap-2">
              <History size={18} className="text-primary-500" />
              Analyses récentes
            </h2>
            <button
              className="text-sm text-primary-500 hover:underline"
              onClick={() => navigate('/historique')}
            >
              Voir tout →
            </button>
          </div>

          {analyses.length === 0 ? (
            <EmptyState
              icon={<Leaf />}
              title="Aucune analyse effectuée"
              description="Lancez votre premier diagnostic pour voir vos résultats ici."
              action={
                <button className="btn-primary" onClick={() => navigate('/diagnostic')}>
                  Premier diagnostic
                </button>
              }
            />
          ) : (
            <div className="space-y-3">
              {analyses.map(a => (
                <AnalyseCard key={a.id_analyse} analyse={a} />
              ))}
            </div>
          )}
        </div>
      </div>
    </Layout>
  )
}

export default DashboardPage