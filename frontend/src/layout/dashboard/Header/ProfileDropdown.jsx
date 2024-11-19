import React, { useState } from "react";
import { Menu, Transition } from "@headlessui/react";
import { usePopper } from "react-popper";
import { NavLink, useNavigate } from "react-router-dom";
import {
    CubeIcon,
    PowerIcon,
    WrenchScrewdriverIcon,
} from "@heroicons/react/24/outline";

function ProfileDropdown() {
    const [referenceElement, setReferenceElement] = useState(null);
    const [popperElement, setPopperElement] = useState(null);
    const navigate = useNavigate();
    let { styles, attributes } = usePopper(referenceElement, popperElement, {
        placement: "bottom-end",
        modifiers: [
            {
                name: "offset",
                options: {
                    offset: [0, 8],
                },
            },
        ],
    });

    // Función para manejar el cierre de sesión
    const handleLogout = async () => {
        try {
            await fetch("http://localhost:8000/auth/logout", {
                method: "POST",
                credentials: 'include', // Asegura que las cookies se envían en la solicitud
            });
            // Redirige al usuario a /login
            navigate("/login");
        } catch (error) {
            console.error("Error al cerrar sesión:", error);
        }
    };

    return (
        <Menu>
            <Menu.Button
                ref={setReferenceElement}
                className="inline-flex h-8 w-8 rounded-full overflow-hidden outline outline-2 outline-offset-2 outline-slate-300 dark:outline-slate-700"
            >
                <img src="/images/avatar/a.jpg" alt="" />
            </Menu.Button>
            <Transition
                enter="transition duration-100 ease-out"
                enterFrom="transform scale-95 opacity-0"
                enterTo="transform scale-100 opacity-100"
                leave="transition duration-75 ease-out"
                leaveFrom="transform scale-100 opacity-100"
                leaveTo="transform scale-95 opacity-0"
            >
                <Menu.Items
                    ref={setPopperElement}
                    style={styles.popper}
                    {...attributes.popper}
                    className="absolute end-0 top-10 w-48 bg-white dark:bg-slate-950 shadow-sm border border-slate-200 dark:border-slate-800 rounded-lg"
                >
                    <div className="p-4 flex items-center">
                        <div className="inline-flex flex-shrink-0 h-10 w-10 rounded-full overflow-hidden outline outline-2 outline-offset-2 outline-slate-300 dark:outline-slate-700">
                            <img src="/images/avatar/a.jpg" alt="" />
                        </div>
                        <div className="ms-4">
                            <h6 className="text-xs font-bold text-slate-700 dark:text-white -mt-0.5">
                                Phillip Burke
                            </h6>
                            <span className="text-[10px] font-bold px-2 py-0.5 rounded-full text-blue-500 bg-blue-100 dark:bg-blue-950">
                                Balance $18.89
                            </span>
                        </div>
                    </div>
                    <ul className="py-2 border-t border-slate-200 dark:border-slate-800">
                        <li>
                            <NavLink
                                to="/"
                                className="flex text-xs px-4 py-2 font-bold text-slate-500 dark:text-slate-200 hover:text-blue-600 hover:dark:text-blue-600 transition-all"
                            >
                                <CubeIcon className="w-4 me-2" />
                                <span>Ir al inicio</span>
                            </NavLink>
                        </li>
                        <li>
                            <NavLink
                                to="/settings"
                                className="flex text-xs px-4 py-2 font-bold text-slate-500 dark:text-slate-200 hover:text-blue-600 hover:dark:text-blue-600 transition-all"
                            >
                                <WrenchScrewdriverIcon className="w-4 me-2" />
                                <span>Configuración</span>
                            </NavLink>
                        </li>
                        <li>
                            <button
                                onClick={handleLogout}
                                className="flex text-xs w-full px-4 py-2 font-bold text-slate-500 dark:text-slate-200 hover:text-blue-600 hover:dark:text-blue-600 transition-all"
                            >
                                <PowerIcon className="w-4 me-2" />
                                <span>Cerrar Sesión</span>
                            </button>
                        </li>
                    </ul>
                </Menu.Items>
            </Transition>
        </Menu>
    );
}

export default ProfileDropdown;
