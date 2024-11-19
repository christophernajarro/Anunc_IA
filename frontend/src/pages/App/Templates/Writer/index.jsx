import React, { useState } from "react";
import parse from 'html-react-parser';
import SimpleBar from "simplebar-react";
import Layout from "../../../../layout/dashboard";
import Section from "../../../../layout/global/Section";
import Container from "../../../../layout/global/Container";
import { Input, Label, Select, Textarea } from "../../../../components";

import { templates } from "../../../../store";
import { NavLink, useParams } from "react-router-dom";
import axios from "axios";
import ReactQuill from "react-quill";
import 'react-quill/dist/quill.snow.css';

const tonos = [
    { name: "Profesional" },
    { name: "Casual" },
    { name: "Divertido" },
    { name: "Emocionado" },
    { name: "Sarcástico" },
    { name: "Femenino" },
    { name: "Masculino" },
    { name: "Misterioso" },
];

const plantillasDeTexto = templates.filter((template) => template.api === "Text");

function Writer() {
    const [tonoSeleccionado, setTonoSeleccionado] = useState(tonos[0]);
    const [nombreProducto, setNombreProducto] = useState("");
    const [descripcionProducto, setDescripcionProducto] = useState("");
    const [palabrasClave, setPalabrasClave] = useState("");
    const [longitudMaxima, setLongitudMaxima] = useState(200);
    const [variantes, setVariantes] = useState(3);
    const [resultado, setResultado] = useState('');
    const [contenidoEditable, setContenidoEditable] = useState('');

    const { writerslug } = useParams();
    const plantilla = templates.filter((template) => template.slug === writerslug)[0];

    const generarEncabezado = async () => {
        try {
            const token = localStorage.getItem("accessToken");

            if (!token) {
                setResultado("Error: No estás autenticado. Por favor, inicia sesión.");
                return;
            }

            const response = await axios.post(
                "http://localhost:8000/content/create_heading",
                {
                    nombreProducto,
                    descripcionProducto,
                    palabrasClave: palabrasClave.split(",").map((word) => word.trim()),
                    estiloEscritura: tonoSeleccionado.name,
                    longitudMaxima,
                    variantes
                },
                {
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                }
            );

            if (response.data && response.data.encabezados) {
                const encabezadosGenerados = `<ol>${response.data.encabezados.map(header => `<li>${header}</li>`).join("")}</ol>`;
                setResultado(encabezadosGenerados);
                setContenidoEditable(encabezadosGenerados);
            } else {
                setResultado("No se recibieron datos válidos desde el servidor.");
            }
        } catch (error) {
            if (error.response) {
                if (error.response.status === 401) {
                    setResultado("Error de autenticación: tu sesión ha expirado o no tienes permisos. Inicia sesión nuevamente.");
                    localStorage.removeItem("accessToken");
                } else if (error.response.status === 422) {
                    setResultado("Error de validación: algunos de los datos proporcionados no son correctos.");
                } else {
                    setResultado(`Error: ${error.response.data.detail || "Ocurrió un error inesperado en el servidor."}`);
                }
            } else if (error.request) {
                setResultado("No se pudo conectar con el servidor. Verifica tu conexión a internet.");
            } else {
                setResultado(`Error inesperado: ${error.message}`);
            }
            console.error("Error al generar el encabezado:", error);
        }
    };

    const nuevaConsulta = () => {
        if (window.confirm("¿Estás seguro de que deseas comenzar una nueva consulta? Se perderán los datos actuales.")) {
            window.location.reload();
        }
    };

    const guardarDocumentoEditado = () => {
        // Aquí puedes agregar la lógica para guardar el documento editado
        console.log("Documento guardado:", contenidoEditable);
        alert("Documento guardado exitosamente.");
    };

    return (
        <Layout title={`${plantilla.name}`}>
            <Section className="py-10">
                <Container>
                    <div className="flex flex-wrap gap-8 xl:flex-nowrap items-start">
                        {/* Sidebar de plantillas */}
                        <div className="w-full xl:w-96 bg-white dark:bg-slate-950 px-7 py-6 rounded-lg border border-slate-200 dark:border-slate-800">
                            <h4 className="text-xl font-bold mb-3 text-slate-700 dark:text-white">Plantillas</h4>
                            <ul className="flex flex-wrap -mx-4 xl:mx-0">
                                {plantillasDeTexto.map((item, index) => (
                                    <li key={index} className="w-full xs:w-1/2 sm:w-1/3 lg:w-1/4 xl:w-full px-4 xs:py-1 xl:px-0 xl:py-0">
                                        <NavLink
                                            onClick={() => {
                                                setResultado('');
                                                setContenidoEditable('');
                                            }}
                                            to={item.link}
                                            className={({ isActive }) =>
                                                isActive
                                                    ? "flex relative isolate before:content-[''] before:-z-10 before:rounded-md before:absolute before:inset-y-0 before:-inset-x-3 before:bg-blue-100 before:dark:bg-blue-950 text-blue-600"
                                                    : "text-slate-500 dark:text-slate-400"
                                            }
                                        >
                                            <div className="flex items-center py-2">
                                                <div className="h-5 me-3">{item.icon}</div>
                                                <span className="text-sm font-medium">
                                                    {item.name}
                                                </span>
                                            </div>
                                        </NavLink>
                                    </li>
                                ))}
                            </ul>
                        </div>
                        {/* Área principal */}
                        <div className="flex flex-wrap lg:flex-nowrap flex-grow-1 w-full bg-white dark:bg-slate-950 rounded-lg border border-slate-200 dark:border-slate-800 xl:max-h-[calc(100vh-theme(space.52))]">
                            {/* Formulario */}
                            <div className="w-full lg:w-2/5 border-b lg:border-e lg:border-b-0 border-slate-200 dark:border-slate-800">
                                <SimpleBar className="p-6 h-full">
                                    <div className="flex items-center pb-2">
                                        <div className="h-6 me-3">{plantilla.icon}</div>
                                        <h5 className="text-lg font-bold text-slate-700 dark:text-white">{plantilla.name}</h5>
                                    </div>
                                    <div className="flex flex-wrap -my-2 -mx-3">
                                        <div className="w-full py-2 px-3">
                                            <Label htmlFor="nombreProducto" className="mb-2">
                                                Nombre del Producto</Label>
                                            <Input
                                                placeholder="Introduce el nombre del producto"
                                                id="nombreProducto"
                                                value={nombreProducto}
                                                onChange={(e) => setNombreProducto(e.target.value)}
                                            />
                                        </div>
                                        <div className="w-full py-2 px-3">
                                            <Label htmlFor="descripcionProducto" className="mb-2">Descripción del Producto</Label>
                                            <Textarea
                                                placeholder="Describe el producto"
                                                id="descripcionProducto"
                                                rows="4"
                                                value={descripcionProducto}
                                                onChange={(e) => setDescripcionProducto(e.target.value)}
                                            />
                                        </div>
                                        <div className="w-full py-2 px-3">
                                            <Label htmlFor="keywords" className="mb-2">
                                                Palabras clave <span className="self-start text-xs text-slate-500 dark:text-slate-400 ms-2 mt-0.5">Separadas por comas</span>
                                            </Label>
                                            <Input
                                                placeholder="Ejemplo: Ecommerce, productividad, engagement"
                                                id="keywords"
                                                value={palabrasClave}
                                                onChange={(e) => setPalabrasClave(e.target.value)}
                                            />
                                        </div>
                                        <div className="w-full sm:w-1/2 lg:w-full py-2 px-3">
                                            <Label htmlFor="tone" className="mb-2">Estilo de Escritura</Label>
                                            <Select
                                                selected={tonoSeleccionado}
                                                options={tonos}
                                                onChange={(value) => setTonoSeleccionado(value)}
                                                id="tone"
                                            />
                                        </div>
                                        <div className="w-full sm:w-1/2 lg:w-full py-2 px-3">
                                            <Label htmlFor="varientes" className="mb-2">Variantes</Label>
                                            <Input
                                                id="varientes"
                                                type="number"
                                                max="3"
                                                value={variantes}
                                                onChange={(e) => setVariantes(parseInt(e.target.value))}
                                            />
                                        </div>
                                        <div className="w-full sm:w-1/2 lg:w-full py-2 px-3">
                                            <Label htmlFor="maxLength" className="mb-2">Longitud Máxima del Resultado</Label>
                                            <Input
                                                id="maxLength"
                                                type="number"
                                                max="200"
                                                value={longitudMaxima}
                                                onChange={(e) => setLongitudMaxima(parseInt(e.target.value))}
                                            />
                                        </div>
                                        <div className="py-2 px-3 flex gap-2">
                                            <button onClick={generarEncabezado} className="inline-flex font-medium text-sm bg-blue-600 text-white hover:bg-blue-800 transition-all px-5 py-2 rounded-full">
                                                Generar
                                            </button>
                                            <button onClick={nuevaConsulta} className="inline-flex font-medium text-sm bg-red-600 text-white hover:bg-red-800 transition-all px-5 py-2 rounded-full">
                                                Nueva Consulta
                                            </button>
                                        </div>
                                    </div>
                                </SimpleBar>
                            </div>
                            {/* Área de resultado editable con ReactQuill */}
                            <div className="w-full lg:w-3/5 flex flex-col">
                                {resultado ? 
                                <SimpleBar className="p-6 h-full">
                                    <div className="flex flex-col h-full">
                                        <ReactQuill
                                            className="flex-grow mb-4"
                                            theme="snow"
                                            value={contenidoEditable}
                                            onChange={setContenidoEditable}
                                        />
                                        <button onClick={guardarDocumentoEditado} className="self-end inline-flex font-medium text-sm bg-green-600 text-white hover:bg-green-800 transition-all px-5 py-2 rounded-full mt-4">
                                            Guardar documento editado
                                        </button>
                                    </div>
                                </SimpleBar>
                                : 
                                <div className="px-6 py-20 h-full w-full flex flex-col items-center justify-center text-center">
                                    <div className="h-16 mb-3">{plantilla.icon}</div>
                                    <div className="text-slate-500 dark:text-slate-400 font-medium">Llena el formulario y presiona Generar.</div>
                                </div>
                                }
                            </div>
                        </div>
                    </div>
                </Container>
            </Section>
        </Layout>
    );
}

export default Writer;