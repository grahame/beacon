import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router";
import { Provider } from "react-redux";
import { store } from "./rtk/store";
import "./index.css";
import "bootstrap/dist/css/bootstrap.min.css";
import App from "./App.tsx";
import { UserProvider } from "./features/auth/UserProvider.tsx";
import { OAuthCallback } from "./features/auth/OAuthCallback.tsx";

createRoot(document.getElementById("root")!).render(
    <Provider store={store}>
        <StrictMode>
            <BrowserRouter>
                <Routes>
                    <Route
                        path="/"
                        element={
                            <UserProvider>
                                <App />
                            </UserProvider>
                        }
                    />
                    <Route path="/oauth-callback" element={<OAuthCallback />} />
                </Routes>
            </BrowserRouter>
        </StrictMode>
    </Provider>
);
