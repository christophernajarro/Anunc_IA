import React, { createContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axiosInstance from "../api/api"; // Asegúrate de que la ruta es correcta

// Crear el contexto
export const AuthContext = createContext();

// Proveedor del contexto
export const AuthProvider = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [isLoading, setIsLoading] = useState(true);
    const navigate = useNavigate();

    // Función para verificar la sesión
    const checkSession = async () => {
        try {
            await axiosInstance.get("/auth/check_session", {
                withCredentials: true, // Asegura que se envíen cookies
            });
            setIsAuthenticated(true);
        } catch (error) {
            console.error("Error al verificar la sesión:", error);
            setIsAuthenticated(false);
        } finally {
            setIsLoading(false);
        }
    };

    // Verificar la sesión al montar el componente
    useEffect(() => {
        checkSession();
    }, []);

    // Función para iniciar sesión
    const login = async (email, password) => {
        try {
            const params = new URLSearchParams();
            params.append('username', email);
            params.append('password', password);
            // No necesitas agregar 'grant_type' a menos que lo requiera tu backend

            const response = await axiosInstance.post("/auth/login", params, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                withCredentials: true, // Asegura que se envíen cookies
            });

            setIsAuthenticated(true);
            navigate("/dashboard");
        } catch (error) {
            // Manejar errores de forma adecuada
            const errorMessage =
                error.response?.data?.detail || "Error en el inicio de sesión";
            throw new Error(errorMessage);
        }
    };

    // Función para cerrar sesión
    const logout = async () => {
        try {
            await axiosInstance.post("/auth/logout", {}, {
                withCredentials: true, // Asegura que se envíen cookies
            });
            setIsAuthenticated(false);
            navigate("/login");
        } catch (error) {
            console.error("Error al cerrar sesión:", error);
        }
    };

    return (
        <AuthContext.Provider value={{ isAuthenticated, isLoading, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};