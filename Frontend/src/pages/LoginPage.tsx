import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { toast } from 'react-toastify';
import { Leaf, Eye, EyeOff, Loader2 } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { LoginRequest, RegisterRequest, Role } from '../types';

type Tab = 'login' | 'register';

const ROLES: { value: Role; label: string }[] = [
  { value: 'agriculteur',    label: 'Agriculteur' },
  { value: 'agronome',       label: 'Agronome / Expert phytosanitaire' },
  { value: 'chercheur',      label: 'Chercheur / Étudiant' },
];

// Formulaire Connexion 
const LoginForm: React.FC<{ onSwitch: () => void }> = ({ onSwitch }) => {
  const { login } = useAuth();
  const navigate   = useNavigate();
  const location   = useLocation();
  const from       = (location.state as { from?: { pathname: string } })?.from?.pathname ?? '/dashboard';

  const [showPwd, setShowPwd] = useState(false);
  const [loading,  setLoading]  = useState(false);

  const { register, handleSubmit, formState: { errors } } = useForm<LoginRequest>();

  const onSubmit = async (data: LoginRequest) => {
    setLoading(true);
    try {
      await login(data);
      toast.success('Connexion réussie !');
      navigate(from, { replace: true });
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { detail?: string } } })
        ?.response?.data?.detail ?? 'Identifiants invalides.';
      toast.error(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Adresse email
        </label>
        <input
          type="email"
          placeholder="votre@email.com"
          className="input-field"
          {...register('email', {
            required: "L'email est obligatoire",
            pattern: { value: /\S+@\S+\.\S+/, message: 'Email invalide' },
          })}
        />
        {errors.email && (
          <p className="text-red-500 text-xs mt-1">{errors.email.message}</p>
        )}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Mot de passe
        </label>
        <div className="relative">
          <input
            type={showPwd ? 'text' : 'password'}
            placeholder="••••••••"
            className="input-field pr-10"
            {...register('password', { required: 'Le mot de passe est obligatoire' })}
          />
          <button
            type="button"
            className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400"
            onClick={() => setShowPwd(!showPwd)}
          >
            {showPwd ? <EyeOff size={16} /> : <Eye size={16} />}
          </button>
        </div>
        {errors.password && (
          <p className="text-red-500 text-xs mt-1">{errors.password.message}</p>
        )}
      </div>

      <button
        type="submit"
        disabled={loading}
        className="btn-primary w-full flex items-center justify-center gap-2"
      >
        {loading && <Loader2 size={16} className="animate-spin" />}
        {loading ? 'Connexion...' : 'Se connecter'}
      </button>

      <p className="text-center text-sm text-gray-500">
        Pas encore de compte ?{' '}
        <button
          type="button"
          className="text-primary-500 hover:underline font-medium"
          onClick={onSwitch}
        >
          S'inscrire
        </button>
      </p>
    </form>
  );
};

//  Formulaire Inscription 
const RegisterForm: React.FC<{ onSwitch: () => void }> = ({ onSwitch }) => {
  const { register: registerUser } = useAuth();
  const navigate   = useNavigate();
  const [showPwd, setShowPwd] = useState(false);
  const [loading, setLoading]  = useState(false);

  const { register, handleSubmit, watch, formState: { errors } } =
    useForm<RegisterRequest & { confirm_password: string }>();

  const onSubmit = async (data: RegisterRequest) => {
    setLoading(true);
    try {
      await registerUser(data);
      toast.success('Compte créé avec succès !');
      navigate('/dashboard');
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { detail?: string } } })
        ?.response?.data?.detail ?? "Erreur lors de l'inscription.";
      toast.error(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Prénom</label>
          <input
            type="text"
            placeholder="Jean"
            className="input-field"
            {...register('prenom', { required: 'Obligatoire' })}
          />
          {errors.prenom && <p className="text-red-500 text-xs mt-1">{errors.prenom.message}</p>}
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Nom</label>
          <input
            type="text"
            placeholder="Dupont"
            className="input-field"
            {...register('nom', { required: 'Obligatoire' })}
          />
          {errors.nom && <p className="text-red-500 text-xs mt-1">{errors.nom.message}</p>}
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
        <input
          type="email"
          placeholder="votre@email.com"
          className="input-field"
          {...register('email', {
            required: 'Obligatoire',
            pattern: { value: /\S+@\S+\.\S+/, message: 'Email invalide' },
          })}
        />
        {errors.email && <p className="text-red-500 text-xs mt-1">{errors.email.message}</p>}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Rôle</label>
        <select
          className="input-field"
          {...register('role', { required: 'Choisissez un rôle' })}
        >
          <option value="">-- Sélectionner --</option>
          {ROLES.map((r) => (
            <option key={r.value} value={r.value}>{r.label}</option>
          ))}
        </select>
        {errors.role && <p className="text-red-500 text-xs mt-1">{errors.role.message}</p>}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Mot de passe
        </label>
        <div className="relative">
          <input
            type={showPwd ? 'text' : 'password'}
            placeholder="Minimum 8 caractères"
            className="input-field pr-10"
            {...register('password', {
              required: 'Obligatoire',
              minLength: { value: 8, message: 'Minimum 8 caractères' },
            })}
          />
          <button
            type="button"
            className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400"
            onClick={() => setShowPwd(!showPwd)}
          >
            {showPwd ? <EyeOff size={16} /> : <Eye size={16} />}
          </button>
        </div>
        {errors.password && <p className="text-red-500 text-xs mt-1">{errors.password.message}</p>}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Confirmer le mot de passe
        </label>
        <input
          type="password"
          placeholder="••••••••"
          className="input-field"
          {...register('confirm_password', {
            validate: (v) =>
              v === watch('password') || 'Les mots de passe ne correspondent pas',
          })}
        />
        {errors.confirm_password && (
          <p className="text-red-500 text-xs mt-1">{errors.confirm_password.message}</p>
        )}
      </div>

      <button
        type="submit"
        disabled={loading}
        className="btn-primary w-full flex items-center justify-center gap-2"
      >
        {loading && <Loader2 size={16} className="animate-spin" />}
        {loading ? 'Inscription...' : "Créer mon compte"}
      </button>

      <p className="text-center text-sm text-gray-500">
        Déjà un compte ?{' '}
        <button
          type="button"
          className="text-primary-500 hover:underline font-medium"
          onClick={onSwitch}
        >
          Se connecter
        </button>
      </p>
    </form>
  );
};

// Page principale 
const LoginPage: React.FC = () => {
  const [tab, setTab] = useState<Tab>('login');

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-600 to-primary-800
                    flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* En-tête */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16
                          bg-white/10 rounded-2xl mb-4">
            <Leaf size={32} className="text-white" />
          </div>
          <h1 className="text-3xl font-bold text-white">CacaoDetect</h1>
          <p className="text-white/70 text-sm mt-1">
            Détection intelligente des maladies du cacaoyer
          </p>
        </div>

        {/* Carte formulaire */}
        <div className="bg-white rounded-2xl shadow-2xl overflow-hidden">
          {/* Onglets */}
          <div className="flex border-b border-gray-100">
            <button
              className={`flex-1 py-4 text-sm font-semibold transition-colors
                ${tab === 'login'
                  ? 'text-primary-500 border-b-2 border-primary-500'
                  : 'text-gray-400 hover:text-gray-600'}`}
              onClick={() => setTab('login')}
            >
              Connexion
            </button>
            <button
              className={`flex-1 py-4 text-sm font-semibold transition-colors
                ${tab === 'register'
                  ? 'text-primary-500 border-b-2 border-primary-500'
                  : 'text-gray-400 hover:text-gray-600'}`}
              onClick={() => setTab('register')}
            >
              Inscription
            </button>
          </div>

          {/* Corps */}
          <div className="p-6">
            {tab === 'login'
              ? <LoginForm  onSwitch={() => setTab('register')} />
              : <RegisterForm onSwitch={() => setTab('login')} />}
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;