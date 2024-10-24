/* eslint-disable no-unused-vars */
/* eslint-disable react/prop-types */
import React, {useEffect} from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import ThemeProvider from "../layout/provider";

//app
import AppDashboard from "../pages/App/Dashboard";
import AdminDashboard from "../pages/Admin/Dashboard";

import { useLocation } from "react-router";

const ScrollToTop = (props) => {
  const location = useLocation();
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [location]);

  return <>{props.children}</>
};

function Router() {
    return (
        <BrowserRouter>
            <ScrollToTop>
                <Routes>
                    <Route element={<ThemeProvider />}>
                        <Route path="dashboard">
                            <Route index element={<AppDashboard />} />
                        </Route>
                        <Route path="app">
                            <Route index element={<AdminDashboard />} />
                        </Route>
                    </Route>
                </Routes>
            </ScrollToTop>
        </BrowserRouter>
    );
}

export default Router;
