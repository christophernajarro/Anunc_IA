import React from "react";
import Layout from "../../../layout/website";
import Section from "../../../layout/global/Section";
import Container from "../../../layout/global/Container";
import { Link } from "react-router-dom";

function IntroPage() {
    return (
        <Layout>
            <Section className="py-24 bg-gradient-to-br from-white dark:from-slate-950 to-blue-100 dark:to-blue-950 overflow-hidden">
                <Container>
                    <div className="max-w-3xl mx-auto text-center">
                        <h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-[2.5rem] font-bold text-slate-800 dark:text-white">
                            <span className="block text-4xl md:text-5xl lg:text-6xl xl:text-7xl text-blue-400 mb-3 lg:mb-6">Anunc IA</span>
                            Plataforma automatizada de publicidad para redes sociales
                        </h1>
                        <p className="mt-8 text-lg text-slate-600 dark:text-slate-400">
                            Anunc IA ayuda a comerciantes en Perú a gestionar y optimizar campañas publicitarias en Facebook, TikTok y Google.
                        </p>
                    </div>

                    <div className="flex justify-center gap-6 mt-12">
                        <Link to="/login" className="p-4 bg-blue-600 text-white rounded-lg text-center">
                            Iniciar Sesión
                        </Link>
                        <Link to="/create-account" className="p-4 bg-green-600 text-white rounded-lg text-center">
                            Registrarse
                        </Link>
                    </div>
                </Container>
            </Section>

            <Section className="py-16 bg-white dark:bg-slate-950">
                <Container>
                    <h2 className="text-3xl font-bold text-center text-slate-800 dark:text-white mb-8">Beneficios de Anunc IA</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        <div className="p-6 bg-slate-100 dark:bg-slate-900 rounded-lg">
                            <h3 className="text-xl font-semibold text-blue-500">Ahorro de Tiempo</h3>
                            <p className="mt-2 text-slate-600 dark:text-slate-400">Automatiza la creación de anuncios y permite enfocarse en otras áreas del negocio.</p>
                        </div>
                        <div className="p-6 bg-slate-100 dark:bg-slate-900 rounded-lg">
                            <h3 className="text-xl font-semibold text-blue-500">Optimización de Resultados</h3>
                            <p className="mt-2 text-slate-600 dark:text-slate-400">IA adapta el contenido de los anuncios para mejorar la conversión y captar el público adecuado.</p>
                        </div>
                        <div className="p-6 bg-slate-100 dark:bg-slate-900 rounded-lg">
                            <h3 className="text-xl font-semibold text-blue-500">Control y Flexibilidad</h3>
                            <p className="mt-2 text-slate-600 dark:text-slate-400">Gestión de campañas desde una única plataforma con métricas en tiempo real.</p>
                        </div>
                        <div className="p-6 bg-slate-100 dark:bg-slate-900 rounded-lg">
                            <h3 className="text-xl font-semibold text-blue-500">Métricas y Resultados</h3>
                            <p className="mt-2 text-slate-600 dark:text-slate-400">Visualización centralizada del rendimiento de campañas y ROI.</p>
                        </div>
                    </div>
                </Container>
            </Section>
        </Layout>
    );
}

export default IntroPage;
