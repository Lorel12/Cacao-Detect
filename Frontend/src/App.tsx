import React from 'react';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { ProtectedRoute } from './components';
import { AuthProvider } from './context/AuthContext';
import AdminPanel from './pages/AdminPanel';
import AnalyseDetailPage from './pages/AnalyseDetailPage';
import DashboardPage from './pages/DashboardPage';
import DiagnosticPage from './pages/DiagnosticPage';
import HistoryPage from './pages/HistoryPage';
import LoginPage from './pages/LoginPage';
import NotFoundPage from './pages/NotFoundPage';

const App: React.FC = () => (
  <AuthProvider>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <DashboardPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/diagnostic"
          element={
            <ProtectedRoute>
              <DiagnosticPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/historique"
          element={
            <ProtectedRoute>
              <HistoryPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/historique/:id"
          element={
            <ProtectedRoute>
              <AnalyseDetailPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin"
          element={
            <ProtectedRoute adminOnly>
              <AdminPanel />
            </ProtectedRoute>
          }
        />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
      <ToastContainer
        position="top-right"
        autoClose={4000}
        hideProgressBar={false}
        newestOnTop
        closeOnClick
        pauseOnHover
        theme="light"
      />
    </BrowserRouter>
  </AuthProvider>
);

export default App;
