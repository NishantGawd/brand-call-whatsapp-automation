import React from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const PrivateRoute: React.FC<{ children: React.ReactElement }> = ({
  children,
}) => {
  const { user, token } = useAuth();

  return user && token ? children : <Navigate to="/login" replace />;
};

export default PrivateRoute;
