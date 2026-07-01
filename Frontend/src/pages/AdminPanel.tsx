import React, { useMemo, useState } from 'react';
import { Activity, Leaf, ShieldCheck, Users, AlertTriangle } from 'lucide-react';
import { Layout } from '../components';
import { useAuth } from '../context/AuthContext';
import { roleLabel } from '../utils';

const mockUsers = [
  { id: 1, nom: 'Diop', prenom: 'Awa', email: 'awa@cacaodetect.com', role: 'agriculteur' as const },
  { id: 2, nom: 'Koffi', prenom: 'Basile', email: 'basile@cacaodetect.com', role: 'agronome' as const },
  { id: 3, nom: 'Moua', prenom: 'Sophie', email: 'sophie@cacaodetect.com', role: 'administrateur' as const },
];

const AdminPanel: React.FC = () => {
  const { user } = useAuth();
  const [users] = useState(mockUsers);

  const stats = useMemo(
    () => [
      { label: 'Utilisateurs actifs', value: users.length, icon: <Users size={18} /> },
      { label: 'Analyses aujourd’hui', value: '128', icon: <Activity size={18} /> },
      { label: 'Détections critiques', value: '14', icon: <AlertTriangle size={18} /> },
      { label: 'Modele stable', value: '98.4%', icon: <ShieldCheck size={18} /> },
    ],
    [users.length]
  );

  return (
    <Layout>
      <div className="space-y-6">
        <div className="rounded-[2rem] border border-stone-200/80 bg-gradient-to-r from-primary-800 to-primary-600 p-8 text-white shadow-premium">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <p className="text-sm uppercase tracking-[0.3em] text-white/70">Administration</p>
              <h1 className="mt-2 text-3xl font-semibold">Bienvenue {user?.prenom ?? 'admin'}</h1>
              <p className="mt-2 max-w-2xl text-sm text-white/80">
                Supervisez les comptes, les performances du modèle et les alertes prioritaires depuis un tableau de bord premium.
              </p>
            </div>
            <div className="rounded-2xl border border-white/20 bg-white/10 p-4">
              <Leaf size={26} />
            </div>
          </div>
        </div>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {stats.map((stat) => (
            <div key={stat.label} className="card flex items-center gap-4">
              <div className="rounded-2xl bg-emerald-50 p-3 text-emerald-700">{stat.icon}</div>
              <div>
                <p className="text-2xl font-semibold text-stone-900">{stat.value}</p>
                <p className="text-sm text-stone-500">{stat.label}</p>
              </div>
            </div>
          ))}
        </div>

        <div className="card">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-stone-900">Gestion des utilisateurs</h2>
            <button className="btn-primary">Ajouter un utilisateur</button>
          </div>
          <div className="overflow-hidden rounded-2xl border border-stone-200">
            <table className="min-w-full divide-y divide-stone-200 text-sm">
              <thead className="bg-stone-50">
                <tr>
                  <th className="px-4 py-3 text-left font-semibold text-stone-600">Nom</th>
                  <th className="px-4 py-3 text-left font-semibold text-stone-600">Email</th>
                  <th className="px-4 py-3 text-left font-semibold text-stone-600">Rôle</th>
                  <th className="px-4 py-3 text-left font-semibold text-stone-600">Statut</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-stone-100 bg-white">
                {users.map((person) => (
                  <tr key={person.id}>
                    <td className="px-4 py-3 font-medium text-stone-800">{person.prenom} {person.nom}</td>
                    <td className="px-4 py-3 text-stone-600">{person.email}</td>
                    <td className="px-4 py-3 text-stone-600">{roleLabel(person.role)}</td>
                    <td className="px-4 py-3">
                      <span className="rounded-full bg-emerald-50 px-2.5 py-1 text-xs font-semibold text-emerald-700">Actif</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default AdminPanel;
