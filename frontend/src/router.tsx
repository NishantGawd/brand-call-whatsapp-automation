// src/router.tsx
import React from "react";
import {
  createBrowserRouter,
  RouterProvider,
  Navigate,
} from "react-router-dom";
import { useAuth } from "./context/AuthContext";
import LoginPage from "./pages/LoginPage";
import DashboardLayout from "./pages/layout/DashboardLayout";
import DashboardPage from "./pages/DashboardPage";
import CallsPage from "./pages/CallsPage";
import ProductsPage from "./pages/ProductsPage";
import AutomationSettingsPage from "./pages/AutomationSettingsPage";
import WhatsAppSettingsPage from "./pages/WhatsappSettingsPage";

const PrivateRoute = ({ children }: { children: React.ReactNode }) => {
  const { token } = useAuth();
  return token ? <>{children}</> : <Navigate to="/login" replace />;
};

const router = createBrowserRouter([
  { path: "/login", element: <LoginPage /> },
  {
    path: "/",
    element: (
      <PrivateRoute>
        <DashboardLayout />
      </PrivateRoute>
    ),
    children: [
      { index: true, element: <DashboardPage /> },
      { path: "calls", element: <CallsPage /> },
      { path: "products", element: <ProductsPage /> },
      { path: "settings/automation", element: <AutomationSettingsPage /> },
      { path: "settings/whatsapp", element: <WhatsAppSettingsPage /> },
    ],
  },
  { path: "*", element: <Navigate to="/" replace /> },
]);

const AppRouter = () => <RouterProvider router={router} />;

export default AppRouter;
