import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Home, SearchX } from 'lucide-react';

const NotFoundPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="flex min-h-screen items-center justify-center bg-[radial-gradient(circle_at_top_left,_rgba(122,91,45,0.18),_transparent_35%),linear-gradient(135deg,_#fcfbf8_0%,_#f4efe6_55%,_#eef4ea_100%)] px-4">
      <div className="card max-w-lg text-center">
        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-emerald-50 text-emerald-700">
          <SearchX size={28} />
        </div>
        <h1 className="mt-6 text-3xl font-semibold text-stone-900">Page introuvable</h1>
        <p className="mt-3 text-sm leading-7 text-stone-600">
          La page que vous recherchez n’existe pas ou a été déplacée. Revenez au tableau de bord pour poursuivre votre diagnostic.
        </p>
        <button className="btn-primary mt-6" onClick={() => navigate('/dashboard')}>
          <Home size={16} className="mr-2" />
          Retour au tableau de bord
        </button>
      </div>
    </div>
  );
};

export default NotFoundPage;
