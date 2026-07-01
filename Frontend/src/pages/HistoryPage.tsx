import React, { useEffect, useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { toast } from 'react-toastify'
import {
  Search, Filter, Trash2, Eye, Download,
  ChevronLeft, ChevronRight, Loader2, Leaf,
} from 'lucide-react'
import { Layout, GraviteBadge, EmptyState, ConfirmDialog } from '../components'
import { analysesService } from '../services/ApiService'
import { AnalyseListItem, FiltresHistorique, Gravite } from '../types'
import { formatDate, formatConfiance, downloadBlob } from '../utils'

const LIMIT = 10

const HistoryPage: React.FC = () => {
  const navigate = useNavigate()

  // ── État 
  const [analyses,    setAnalyses]    = useState<AnalyseListItem[]>([])
  const [total,       setTotal]       = useState(0)
  const [loading,     setLoading]     = useState(true)
  const [exporting,   setExporting]   = useState<number | null>(null)
  const [toDelete,    setToDelete]    = useState<number | null>(null)
  const [filtres, setFiltres] = useState<FiltresHistorique>({
    page: 1, limit: LIMIT,
  })

  // Filtres locaux (inputs contrôlés)
  const [maladieInput,    setMaladieInput]    = useState('')
  const [graviteInput,    setGraviteInput]    = useState<Gravite | ''>('')
  const [dateDebutInput,  setDateDebutInput]  = useState('')
  const [dateFinInput,    setDateFinInput]    = useState('')

  // ── Chargement 
  const fetchAnalyses = useCallback(async (f: FiltresHistorique) => {
    setLoading(true)
    try {
      const res = await analysesService.list(f)
      setAnalyses(res.data.analyses)
      setTotal(res.data.total)
    } catch {
      toast.error('Impossible de charger l\'historique.')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { fetchAnalyses(filtres) }, [filtres, fetchAnalyses])

  // ── Appliquer filtres 
  const appliquerFiltres = () => {
    setFiltres({
      page: 1, limit: LIMIT,
      maladie:    maladieInput || undefined,
      gravite:    graviteInput || undefined,
      date_debut: dateDebutInput || undefined,
      date_fin:   dateFinInput || undefined,
    })
  }

  const reinitialiserFiltres = () => {
    setMaladieInput(''); setGraviteInput('')
    setDateDebutInput(''); setDateFinInput('')
    setFiltres({ page: 1, limit: LIMIT })
  }

  // ── Pagination 
  const totalPages = Math.ceil(total / LIMIT)
  const goPage = (p: number) => setFiltres(f => ({ ...f, page: p }))

  // ── Suppression 
  const confirmerSuppression = async () => {
    if (!toDelete) return
    try {
      await analysesService.delete(toDelete)
      toast.success('Analyse supprimée.')
      fetchAnalyses(filtres)
    } catch {
      toast.error('Erreur lors de la suppression.')
    } finally {
      setToDelete(null)
    }
  }

  // ── Export PDF 
  const exporterPDF = async (id: number) => {
    setExporting(id)
    try {
      const res = await analysesService.exportPDF(id)
      downloadBlob(res.data, `cacaodetect_analyse_${id}.pdf`)
      toast.success('Rapport téléchargé.')
    } catch {
      toast.error('Export impossible.')
    } finally {
      setExporting(null)
    }
  }

  // ── Rendu 
  return (
    <Layout>
      <div className="space-y-6">

        {/* Titre */}
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Historique des analyses</h1>
          <p className="text-gray-500 text-sm mt-1">
            {total} analyse{total > 1 ? 's' : ''} au total
          </p>
        </div>

        {/* Barre de filtres */}
        <div className="card space-y-4">
          <div className="flex items-center gap-2 text-sm font-medium text-gray-700">
            <Filter size={16} className="text-primary-500" />
            Filtres
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div className="relative">
              <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2
                                          text-gray-400" />
              <input
                type="text"
                placeholder="Maladie..."
                className="input-field pl-8 text-sm"
                value={maladieInput}
                onChange={e => setMaladieInput(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && appliquerFiltres()}
              />
            </div>
            <select
              className="input-field text-sm"
              value={graviteInput}
              onChange={e => setGraviteInput(e.target.value as Gravite | '')}
            >
              <option value="">Toutes gravités</option>
              <option value="faible">Faible</option>
              <option value="modere">Modéré</option>
              <option value="eleve">Élevé</option>
            </select>
            <input
              type="date"
              className="input-field text-sm"
              value={dateDebutInput}
              onChange={e => setDateDebutInput(e.target.value)}
            />
            <input
              type="date"
              className="input-field text-sm"
              value={dateFinInput}
              onChange={e => setDateFinInput(e.target.value)}
            />
          </div>
          <div className="flex gap-2">
            <button className="btn-primary text-sm py-2" onClick={appliquerFiltres}>
              Appliquer
            </button>
            <button className="btn-secondary text-sm py-2" onClick={reinitialiserFiltres}>
              Réinitialiser
            </button>
          </div>
        </div>

        {/* Tableau */}
        {loading ? (
          <div className="flex justify-center py-16">
            <Loader2 size={32} className="animate-spin text-primary-400" />
          </div>
        ) : analyses.length === 0 ? (
          <EmptyState
            icon={<Leaf />}
            title="Aucune analyse trouvée"
            description="Modifiez vos filtres ou effectuez votre premier diagnostic."
          />
        ) : (
          <>
            {/* Vue desktop : tableau */}
            <div className="hidden md:block overflow-x-auto rounded-xl border
                            border-gray-100 shadow-sm">
              <table className="w-full text-sm">
                <thead className="bg-gray-50 border-b border-gray-100">
                  <tr>
                    {['Date', 'Maladie', 'Gravité', 'Confiance', 'Statut', 'Actions']
                      .map(h => (
                      <th key={h} className="text-left px-4 py-3 text-xs font-semibold
                                             text-gray-500 uppercase tracking-wide">
                        {h}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-50 bg-white">
                  {analyses.map(a => (
                    <tr key={a.id_analyse} className="hover:bg-gray-50 transition-colors">
                      <td className="px-4 py-3 text-gray-700 whitespace-nowrap">
                        {formatDate(a.date_heure)}
                      </td>
                      <td className="px-4 py-3 font-medium text-gray-900">
                        {a.maladie_nom ?? <span className="text-green-600">Saine</span>}
                      </td>
                      <td className="px-4 py-3">
                        <GraviteBadge gravite={a.niveau_gravite} />
                      </td>
                      <td className="px-4 py-3 text-gray-600">
                        {formatConfiance(a.score_confiance)}
                      </td>
                      <td className="px-4 py-3">
                        <span className={`text-xs px-2 py-0.5 rounded-full font-medium
                          ${a.statut === 'termine' ? 'bg-green-50 text-green-700' :
                            a.statut === 'erreur'  ? 'bg-red-50 text-red-700' :
                                                     'bg-yellow-50 text-yellow-700'}`}>
                          {a.statut === 'termine' ? 'Terminé' :
                           a.statut === 'erreur'  ? 'Erreur' : 'En cours'}
                        </span>
                      </td>
                      <td className="px-4 py-3">
                        <div className="flex items-center gap-1">
                          <button
                            title="Voir le détail"
                            className="p-1.5 text-gray-400 hover:text-primary-500
                                       hover:bg-primary-50 rounded-md transition-colors"
                            onClick={() => navigate(`/historique/${a.id_analyse}`)}
                          >
                            <Eye size={15} />
                          </button>
                          <button
                            title="Exporter PDF"
                            className="p-1.5 text-gray-400 hover:text-green-600
                                       hover:bg-green-50 rounded-md transition-colors"
                            onClick={() => exporterPDF(a.id_analyse)}
                            disabled={exporting === a.id_analyse}
                          >
                            {exporting === a.id_analyse
                              ? <Loader2 size={15} className="animate-spin" />
                              : <Download size={15} />}
                          </button>
                          <button
                            title="Supprimer"
                            className="p-1.5 text-gray-400 hover:text-red-500
                                       hover:bg-red-50 rounded-md transition-colors"
                            onClick={() => setToDelete(a.id_analyse)}
                          >
                            <Trash2 size={15} />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Vue mobile : cartes */}
            <div className="md:hidden space-y-3">
              {analyses.map(a => (
                <div key={a.id_analyse} className="card p-4 space-y-2">
                  <div className="flex items-center justify-between">
                    <p className="font-semibold text-gray-900 text-sm">
                      {a.maladie_nom ?? 'Plante saine'}
                    </p>
                    <GraviteBadge gravite={a.niveau_gravite} />
                  </div>
                  <p className="text-xs text-gray-400">{formatDate(a.date_heure)}</p>
                  <div className="flex gap-2 pt-1">
                    <button className="btn-secondary text-xs py-1.5 px-3 flex-1"
                      onClick={() => navigate(`/historique/${a.id_analyse}`)}>
                      Voir
                    </button>
                    <button className="btn-secondary text-xs py-1.5 px-3 flex-1"
                      onClick={() => exporterPDF(a.id_analyse)}>
                      PDF
                    </button>
                    <button className="btn-danger text-xs py-1.5 px-3"
                      onClick={() => setToDelete(a.id_analyse)}>
                      <Trash2 size={13} />
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex items-center justify-between">
                <p className="text-sm text-gray-500">
                  Page {filtres.page} sur {totalPages}
                </p>
                <div className="flex items-center gap-1">
                  <button
                    className="p-2 rounded-lg border border-gray-200 hover:bg-gray-50
                               disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
                    disabled={filtres.page <= 1}
                    onClick={() => goPage(filtres.page - 1)}
                  >
                    <ChevronLeft size={16} />
                  </button>
                  {Array.from({ length: Math.min(totalPages, 5) }, (_, i) => {
                    const p = i + 1
                    return (
                      <button
                        key={p}
                        className={`w-9 h-9 rounded-lg text-sm font-medium transition-colors
                          ${filtres.page === p
                            ? 'bg-primary-500 text-white'
                            : 'border border-gray-200 hover:bg-gray-50 text-gray-700'}`}
                        onClick={() => goPage(p)}
                      >
                        {p}
                      </button>
                    )
                  })}
                  <button
                    className="p-2 rounded-lg border border-gray-200 hover:bg-gray-50
                               disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
                    disabled={filtres.page >= totalPages}
                    onClick={() => goPage(filtres.page + 1)}
                  >
                    <ChevronRight size={16} />
                  </button>
                </div>
              </div>
            )}
          </>
        )}
      </div>

      {/* Dialogue de confirmation de suppression */}
      <ConfirmDialog
        open={toDelete !== null}
        title="Supprimer cette analyse ?"
        message="Cette action est irréversible. L'analyse et son image annotée seront définitivement supprimées."
        onConfirm={confirmerSuppression}
        onCancel={() => setToDelete(null)}
        danger
      />
    </Layout>
  )
}

export default HistoryPage