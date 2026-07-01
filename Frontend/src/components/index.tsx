import React, { ReactNode } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { Leaf, LogOut, History, LayoutDashboard, Settings, Menu, X } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { Gravite } from '../types';
import { graviteLabel, graviteBgColor } from '../utils';

//  LoadingSpinner
export const LoadingSpinner: React.FC<{ message?: string }> = ({
  message = 'Chargement...',
}) => (
  <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 gap-4">
    <div className="w-12 h-12 border-4 border-primary-200 border-t-primary-500 rounded-full animate-spin" />
    <p className="text-gray-500 text-sm">{message}</p>
  </div>
);

//  ProtectedRoute — Redirige vers /login si non connecté
export const ProtectedRoute: React.FC<{
  children: ReactNode;
  adminOnly?: boolean;
}> = ({ children, adminOnly = false }) => {
  const { isAuthenticated, isLoading, user } = useAuth();
  const location = useLocation();

  if (isLoading) return <LoadingSpinner />;
  if (!isAuthenticated) return <Navigate to="/login" state={{ from: location }} replace />;
  if (adminOnly && user?.role !== 'administrateur')
    return <Navigate to="/dashboard" replace />;

  return <>{children}</>;
};

//  GraviteBadge
export const GraviteBadge: React.FC<{ gravite: Gravite | null | undefined }> = ({
  gravite,
}) => (
  <span
    className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border ${graviteBgColor(gravite)}`}
  >
    {gravite ? graviteLabel(gravite) : 'Sain'}
  </span>
);

//  Navbar
export const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const [menuOpen, setMenuOpen] = React.useState(false);

  const navLinks = [
    { to: '/diagnostic', label: 'Diagnostic', icon: <Leaf size={16} /> },
    { to: '/dashboard',  label: 'Tableau de bord', icon: <LayoutDashboard size={16} /> },
    { to: '/historique', label: 'Historique', icon: <History size={16} /> },
    ...(user?.role === 'administrateur'
      ? [{ to: '/admin', label: 'Administration', icon: <Settings size={16} /> }]
      : []),
  ];

  const current = window.location.pathname;

  return (
    <nav className="bg-primary-500 text-white shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <a href="/dashboard" className="flex items-center gap-2 font-bold text-lg">
            <Leaf size={22} />
            CacaoDetect
          </a>

          {/* Navigation desktop */}
          <div className="hidden md:flex items-center gap-1">
            {navLinks.map((link) => (
              <a
                key={link.to}
                href={link.to}
                className={`flex items-center gap-1.5 px-3 py-2 rounded-md text-sm font-medium transition-colors
                  ${current === link.to
                    ? 'bg-white/20 text-white'
                    : 'text-white/80 hover:bg-white/10 hover:text-white'}`}
              >
                {link.icon}
                {link.label}
              </a>
            ))}
          </div>

          {/* User + logout (desktop) */}
          <div className="hidden md:flex items-center gap-3">
            <span className="text-sm text-white/80">
              {user?.prenom} {user?.nom}
            </span>
            <button
              onClick={logout}
              className="flex items-center gap-1.5 text-sm text-white/80
                         hover:text-white hover:bg-white/10 px-3 py-2 rounded-md
                         transition-colors"
            >
              <LogOut size={16} />
              Déconnexion
            </button>
          </div>

          {/* Burger mobile */}
          <button
            className="md:hidden p-2 rounded-md hover:bg-white/10"
            onClick={() => setMenuOpen(!menuOpen)}
          >
            {menuOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>

        {/* Menu mobile */}
        {menuOpen && (
          <div className="md:hidden pb-3 pt-1 border-t border-white/20 space-y-1">
            {navLinks.map((link) => (
              <a
                key={link.to}
                href={link.to}
                className="flex items-center gap-2 px-3 py-2 rounded-md text-sm
                           text-white/90 hover:bg-white/10"
                onClick={() => setMenuOpen(false)}
              >
                {link.icon}
                {link.label}
              </a>
            ))}
            <button
              onClick={() => { logout(); setMenuOpen(false); }}
              className="flex items-center gap-2 w-full text-left px-3 py-2
                         rounded-md text-sm text-white/90 hover:bg-white/10"
            >
              <LogOut size={16} />
              Déconnexion
            </button>
          </div>
        )}
      </div>
    </nav>
  );
};

//  Layout — Enveloppe avec Navbar
export const Layout: React.FC<{ children: ReactNode }> = ({ children }) => (
  <div className="min-h-screen bg-gray-50">
    <Navbar />
    <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {children}
    </main>
  </div>
);

//  ConfirmDialog — Dialogue de confirmation
export const ConfirmDialog: React.FC<{
  open: boolean;
  title: string;
  message: string;
  onConfirm: () => void;
  onCancel: () => void;
  danger?: boolean;
}> = ({ open, title, message, onConfirm, onCancel, danger = false }) => {
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
      <div className="bg-white rounded-xl shadow-xl max-w-sm w-full p-6">
        <h3 className="font-semibold text-gray-900 text-lg mb-2">{title}</h3>
        <p className="text-gray-600 text-sm mb-6">{message}</p>
        <div className="flex gap-3 justify-end">
          <button className="btn-secondary" onClick={onCancel}>Annuler</button>
          <button
            className={danger ? 'btn-danger' : 'btn-primary'}
            onClick={onConfirm}
          >
            Confirmer
          </button>
        </div>
      </div>
    </div>
  );
};

//  EmptyState
export const EmptyState: React.FC<{
  icon?: ReactNode;
  title: string;
  description?: string;
  action?: ReactNode;
}> = ({ icon, title, description, action }) => (
  <div className="flex flex-col items-center justify-center py-16 gap-4 text-center">
    {icon && <div className="text-gray-300 text-6xl">{icon}</div>}
    <h3 className="text-gray-700 font-semibold text-lg">{title}</h3>
    {description && <p className="text-gray-400 text-sm max-w-xs">{description}</p>}
    {action && <div className="mt-2">{action}</div>}
  </div>
);

//  StatCard — Carte statistique simple
export const StatCard: React.FC<{
  label: string;
  value: string | number;
  icon: ReactNode;
  color?: string;
}> = ({ label, value, icon, color = 'text-primary-500' }) => (
  <div className="card flex items-center gap-4">
    <div className={`p-3 rounded-xl bg-gray-50 ${color}`}>{icon}</div>
    <div>
      <p className="text-2xl font-bold text-gray-900">{value}</p>
      <p className="text-sm text-gray-500">{label}</p>
    </div>
  </div>
);