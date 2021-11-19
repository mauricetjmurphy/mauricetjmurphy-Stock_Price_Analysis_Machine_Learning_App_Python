import React, { useState, useHistory } from "react";
import "./App.css";
import Footer from "./components/Footer";
import { Routes, Route, useLocation } from "react-router-dom";
import TopNavbar from "./components/TopNavbar";

import HomePage from "./pages/home-page/HomePage";
import SentimentPage from "./pages/sentiment-page/SentimentPage";
import LoginPage from "./pages/login-page/LoginPage";
import RegisterPage from "./pages/register-page/RegisterPage";

function App() {
    const location = useLocation();

    return (
        <div className="App">
            {location.pathname !== "/" && location.pathname !== "/register" ? (
                <TopNavbar />
            ) : null}

            <Routes>
                <Route path="/" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route path="/home" element={<HomePage />} exact />
                <Route path="/sentiment" element={<SentimentPage />} />
            </Routes>

            {location.pathname != "/" && location.pathname != "/register" ? (
                <Footer />
            ) : null}
        </div>
    );
}

export default App;
