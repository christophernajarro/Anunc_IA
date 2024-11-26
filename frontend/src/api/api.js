import axios from "axios";

const axiosInstance = axios.create({
    //baseURL: "https://kvpkimi65a3umrcqhbfnkqg2ma0yeare.lambda-url.us-east-2.on.aws", // Cambia al dominio correcto
    baseURL: "http://localhost:8000",
    headers: {
        "Content-Type": "application/json",
    },
    withCredentials: true, // Asegura que se envíen cookies o credenciales
});

export default axiosInstance;