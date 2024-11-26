import React, { useState, useContext } from "react";
import { AuthContext } from "../../../context/AuthContext";
import { useNavigate } from "react-router-dom";
import Layout from "../../../layout/website";
import Section from "../../../layout/global/Section";
import Container from "../../../layout/global/Container";
import { Label, Input, Button } from "../../../components";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faFacebookF, faGoogle } from "@fortawesome/free-brands-svg-icons";
import axiosInstance from "../../../api/api"; // Importa axiosInstance

function CreateAccountPage() {
    const [nombre, setNombre] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
    const [successMessage, setSuccessMessage] = useState("");
    const { login } = useContext(AuthContext);
    const navigate = useNavigate();

    const handleRegister = async (e) => {
        e.preventDefault();
        setErrorMessage("");
        setSuccessMessage("");

        if (password !== confirmPassword) {
            setErrorMessage("Las contraseñas no coinciden");
            return;
        }

        try {
            const response = await axiosInstance.post("/auth/register", {
                nombre,
                email,
                password
            }, {
                withCredentials: true, // Asegura que se envíen cookies
            });

            setSuccessMessage("Registro exitoso. Redirigiendo al dashboard...");

            // Opcional: Iniciar sesión automáticamente después del registro
            await login(email, password);
        } catch (error) {
            if (error.response) {
                setErrorMessage(error.response.data.detail || "Error en el registro");
            } else {
                setErrorMessage("Error en el registro, por favor intente más tarde");
            }
            console.error("Error:", error);
        }
    };

    return (
        <Layout title="Crear Cuenta">
            <Section className="py-10 my-auto">
                <Container>
                    <div className="flex justify-center -mx-3">
                        <div className="w-full xs:w-4/5 sm:w-3/5 md:w-1/2 lg:w-2/5 xl:w-1/3 px-3">
                            <div className="bg-white dark:bg-slate-950 rounded-lg border border-slate-200 dark:border-slate-800 w-full p-6 pt-5">
                                <div className="mb-2">
                                    <h3 className="text-xl font-bold text-slate-700 dark:text-white mb-1">
                                        Crear Cuenta
                                    </h3>
                                    <p className="text-sm text-slate-500 dark:text-slate-400">
                                        Verifica tu información
                                    </p>
                                </div>
                                {errorMessage && (
                                    <p className="text-red-500 text-sm">{errorMessage}</p>
                                )}
                                {successMessage && (
                                    <p className="text-green-500 text-sm">{successMessage}</p>
                                )}
                                <form onSubmit={handleRegister}>
                                    <div className="py-2">
                                        <Label htmlFor="nombre-completo" className="mb-2">
                                            Nombre Completo
                                        </Label>
                                        <Input
                                            placeholder="Carlos Balbuena"
                                            id="nombre-completo"
                                            value={nombre}
                                            onChange={(e) => setNombre(e.target.value)}
                                        />
                                    </div>
                                    <div className="py-2">
                                        <Label htmlFor="correo-electronico" className="mb-2">
                                            Correo Electrónico
                                        </Label>
                                        <Input
                                            placeholder="ejemplo@gmail.com"
                                            id="correo-electronico"
                                            value={email}
                                            onChange={(e) => setEmail(e.target.value)}
                                        />
                                    </div>
                                    <div className="py-2">
                                        <Label htmlFor="contrasena" className="mb-2">
                                            Contraseña
                                        </Label>
                                        <Input
                                            id="contrasena"
                                            type="password"
                                            value={password}
                                            onChange={(e) => setPassword(e.target.value)}
                                        />
                                    </div>
                                    <div className="py-2">
                                        <Label htmlFor="confirmar-contrasena" className="mb-2">
                                            Confirmar Contraseña
                                        </Label>
                                        <Input
                                            id="confirmar-contrasena"
                                            type="password"
                                            value={confirmPassword}
                                            onChange={(e) => setConfirmPassword(e.target.value)}
                                        />
                                    </div>
                                    <div className="pt-3">
                                        <Button type="submit" block className="bg-blue-600 text-white hover:bg-blue-800">
                                            Crear Cuenta
                                        </Button>
                                    </div>
                                </form>
                                <div className="mt-5 mb-4">
                                    <h6 className="text-slate-400 text-[11px] uppercase text-center font-bold tracking-wider">
                                        Registrarse Con
                                    </h6>
                                </div>
                                <div className="flex flex-wrap -mx-3">
                                    <div className="w-1/2 px-3">
                                        <Button
                                            block
                                            className="bg-white dark:bg-slate-950 text-slate-600 dark:text-slate-200 hover:bg-blue-100 hover:dark:bg-blue-950 hover:text-blue-600 hover:dark:text-blue-600 border border-slate-200 dark:border-slate-800 hover:dark:border-blue-950"
                                        >
                                            <FontAwesomeIcon icon={faGoogle} />
                                            <span>Google</span>
                                        </Button>
                                    </div>
                                    <div className="w-1/2 px-3">
                                        <Button
                                            block
                                            className="bg-white dark:bg-slate-950 text-slate-600 dark:text-slate-200 hover:bg-blue-100 hover:dark:bg-blue-950 hover:text-blue-600 hover:dark:text-blue-600 border border-slate-200 dark:border-slate-800 hover:dark:border-blue-950"
                                        >
                                            <FontAwesomeIcon icon={faFacebookF} />
                                            <span>Facebook</span>
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </Container>
            </Section>
        </Layout>
    );
}

export default CreateAccountPage;
