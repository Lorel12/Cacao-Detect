import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
  ReactNode,
} from 'react';
import { Utilisateur, LoginRequest, RegisterRequest } from '../types';
import { authService } from '../services/ApiService';

// ── Forme du contexte 
interface AuthContextType {
  user: Utilisateur | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login:    (data: LoginRequest)    => Promise<void>;
  register: (data: RegisterRequest) => Promise<void>;
  logout:   ()                      => Promise<void>;
}

// ── Création du contexte 
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// ── Provider 
export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user,      setUser]      = useState<Utilisateur | null>(null);
  const [token,     setToken]     = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Restauration de la session depuis localStorage
  useEffect(() => {
    const storedToken = localStorage.getItem('access_token');
    const storedUser  = localStorage.getItem('user');
    if (storedToken && storedUser) {
      try {
        setToken(storedToken);
        setUser(JSON.parse(storedUser));
      } catch {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
      }
    }
    setIsLoading(false);
  }, []);

  // ── LOGIN 
  const login = useCallback(async (data: LoginRequest) => {
    const response = await authService.login(data);
    const { access_token, user: utilisateur } = response.data;
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('user', JSON.stringify(utilisateur));
    setToken(access_token);
    setUser(utilisateur);
  }, []);

  // ── REGISTER 
  const register = useCallback(async (data: RegisterRequest) => {
    const response = await authService.register(data);
    const { access_token, user: utilisateur } = response.data;
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('user', JSON.stringify(utilisateur));
    setToken(access_token);
    setUser(utilisateur);
  }, []);

  // ── LOGOUT 
  const logout = useCallback(async () => {
    try {
      await authService.logout();
    } catch {
      // Peu importe si le backend échoue, on nettoie côté client
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      setToken(null);
      setUser(null);
    }
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!token && !!user,
        isLoading,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

// ── Hook d'accès au contexte 
export const useAuth = (): AuthContextType => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth doit être utilisé dans AuthProvider');
  return ctx;
};

export default AuthContext;