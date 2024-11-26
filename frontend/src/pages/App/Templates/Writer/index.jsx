import React, { useState } from "react";
import SimpleBar from "simplebar-react";
import Layout from "../../../../layout/dashboard";
import Section from "../../../../layout/global/Section";
import Container from "../../../../layout/global/Container";
import { Input, Label, Select, Textarea } from "../../../../components";
import { templates } from "../../../../store";
import { NavLink, useParams, useNavigate, useLocation } from "react-router-dom"; //agregar useNavigate
import axiosInstance from "../../../../api/api";
import ReactQuill from "react-quill";
import "react-quill/dist/quill.snow.css";
import { formatByTemplate } from "../../../../utilities/formatByTemplate";

function Writer() {
    const { writerslug } = useParams();
    const plantilla = templates.find((template) => template.slug === writerslug) || templates[0];

    const initialFields = (plantilla.customFields || []).reduce((acc, field) => {
        acc[field.id] = field.type === "number" ? 0 : "";
        return acc;
    }, {});

    const [fields, setFields] = useState(initialFields);
    const [resultado, setResultado] = useState("");
    const [contenidoEditable, setContenidoEditable] = useState("");

    const handleFieldChange = (id, value) => {
        setFields((prev) => ({ ...prev, [id]: value }));
    };

    const generarResultado = async () => {
        try {
            const requestData = { ...fields };

            if (requestData.palabrasClave) {
                requestData.palabrasClave = requestData.palabrasClave
                    .split(",")
                    .map((word) => word.trim());
            }

            const response = await axiosInstance.post(plantilla.api, requestData);
            if (response.data) {
                const formattedResponse = formatByTemplate(plantilla.slug, response.data);
                setResultado(formattedResponse);
                setContenidoEditable(formattedResponse);
            } else {
                setResultado("<p>No se recibieron datos válidos desde el servidor.</p>");
            }
        } catch (error) {
            const errorMessage =
                error.response?.data?.detail?.[0]?.msg || error.message || "Error desconocido";
            setResultado(`<p>Error: ${errorMessage}</p>`);
            console.error("Error al generar el resultado:", error);
        }
    };

    const nuevaConsulta = () => {
        if (window.confirm("¿Estás seguro de que deseas comenzar una nueva consulta? Se perderán los datos actuales.")) {
            setFields(initialFields);
            setResultado("");
            setContenidoEditable("");
        }
    };

    //Secuencialidad de pasos
    const navigate = useNavigate(); //agregar useNavigate
    const location = useLocation();

    const steps = [
        "/template/define-campaign",
        "/template/define-audience",
        "/template/choose-format-cta",
        "/template/create-creative-content",
        "/template/create-heading",
    ];

    const currentStepIndex = steps.indexOf(location.pathname);

    const avanzarPaso = () => {
        if (currentStepIndex < steps.length - 1) {
            navigate(steps[currentStepIndex + 1]); // Avanza al siguiente paso
        } else {
            alert("Todos los pasos han sido completados.");
            navigate("/documents"); // Redirige a /documents al completar todos los pasos
        }
    };

    const guardarDocumentoEditado = () => {
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
                            <h4 className="text-xl font-bold mb-3 text-slate-700 dark:text-white">
                                Plantillas
                            </h4>
                            <ul className="flex flex-wrap -mx-4 xl:mx-0">
                                {templates.map((item, index) => (
                                    <li
                                        key={index}
                                        className="w-full xs:w-1/2 sm:w-1/3 lg:w-1/4 xl:w-full px-4 xs:py-1 xl:px-0 xl:py-0"
                                    >
                                        <NavLink
                                            to={item.link}
                                            className={({ isActive }) =>
                                                isActive
                                                    ? "flex relative isolate before:content-[''] before:-z-10 before:rounded-md before:absolute before:inset-y-0 before:-inset-x-3 before:bg-blue-100 before:dark:bg-blue-950 text-blue-600"
                                                    : "text-slate-500 dark:text-slate-400"
                                            }
                                        >
                                            <div className="flex items-center py-2">
                                                <div className="h-5 me-3">{item.icon}</div>
                                                <span className="text-sm font-medium">{item.name}</span>
                                            </div>
                                        </NavLink>
                                    </li>
                                ))}
                            </ul>
                        </div>
                        {/* Área principal */}
                        <div className="flex flex-wrap lg:flex-nowrap flex-grow-1 w-full bg-white dark:bg-slate-950 rounded-lg border border-slate-200 dark:border-slate-800 xl:max-h-[calc(100vh-theme(space.52))]">
                            {/* Formulario dinámico */}
                            <div className="w-full lg:w-2/5 border-b lg:border-e lg:border-b-0 border-slate-200 dark:border-slate-800">
                                <SimpleBar className="p-6 h-full">
                                    <div className="flex items-center pb-2">
                                        <div className="h-6 me-3">{plantilla.icon}</div>
                                        <h5 className="text-lg font-bold text-slate-700 dark:text-white">
                                            {plantilla.name}
                                        </h5>
                                    </div>
                                    <div className="flex flex-wrap -my-2 -mx-3">
                                        {(plantilla.customFields || []).map((field) => (
                                            <div key={field.id} className="w-full py-2 px-3">
                                                <Label htmlFor={field.id} className="mb-2">
                                                    {field.label}
                                                </Label>
                                                {field.type === "select" ? (
                                                    <Select
                                                        id={field.id}
                                                        options={field.options.map((option) => ({
                                                            name: option,
                                                        }))}
                                                        selected={{ name: fields[field.id] }}
                                                        onChange={(value) =>
                                                            handleFieldChange(field.id, value.name)
                                                        }
                                                    />
                                                ) : field.type === "textarea" ? (
                                                    <Textarea
                                                        id={field.id}
                                                        rows="4"
                                                        placeholder={field.placeholder}
                                                        value={fields[field.id]}
                                                        onChange={(e) =>
                                                            handleFieldChange(field.id, e.target.value)
                                                        }
                                                    />
                                                ) : (
                                                    <Input
                                                        id={field.id}
                                                        type={field.type}
                                                        placeholder={field.placeholder}
                                                        value={fields[field.id]}
                                                        onChange={(e) =>
                                                            handleFieldChange(field.id, e.target.value)
                                                        }
                                                    />
                                                )}
                                            </div>
                                        ))}
                                        <div className="py-2 px-3 flex gap-2">
                                            <button
                                                onClick={generarResultado}
                                                className="inline-flex font-medium text-sm bg-blue-600 text-white hover:bg-blue-800 transition-all px-5 py-2 rounded-full"
                                            >
                                                Generar
                                            </button>
                                            <button
                                                onClick={nuevaConsulta}
                                                className="inline-flex font-medium text-sm bg-red-600 text-white hover:bg-red-800 transition-all px-5 py-2 rounded-full"
                                            >
                                                Nueva Consulta
                                            </button>
                                        </div>
                                    </div>
                                </SimpleBar>
                            </div>
                            {/* Área de resultado editable */}
                            <div className="w-full lg:w-3/5 flex flex-col">
                                {resultado ? (
                                    <SimpleBar className="p-6 h-full">
                                        <div className="flex flex-col h-full">
                                            <ReactQuill
                                                className="flex-grow mb-4"
                                                theme="snow"
                                                value={contenidoEditable}
                                                onChange={setContenidoEditable}
                                            />
                                            <button
                                                onClick={() => { guardarDocumentoEditado(); avanzarPaso(); }}
                                                className="self-end inline-flex font-medium text-sm bg-green-600 text-white hover:bg-green-800 transition-all px-5 py-2 rounded-full mt-4"
                                            >
                                                Guardar documento editado
                                            </button>
                                        </div>
                                    </SimpleBar>
                                ) : (
                                    <div className="px-6 py-20 h-full w-full flex flex-col items-center justify-center text-center">
                                        <div className="h-16 mb-3">{plantilla.icon}</div>
                                        <div className="text-slate-500 dark:text-slate-400 font-medium">
                                            Llena el formulario y presiona Generar.
                                        </div>
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                </Container>
            </Section>
        </Layout>
    );
}

export default Writer;
