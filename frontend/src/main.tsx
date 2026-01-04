import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { store } from "./rtk/store";
import { Provider } from "react-redux";
import "./index.css";
import "bootstrap/dist/css/bootstrap.min.css";
import App from "./App.tsx";
import { UserProvider } from "./features/auth/UserProvider.tsx";

createRoot(document.getElementById("root")!).render(
    <Provider store={store}>
        <StrictMode>
            <UserProvider>
                <App />
            </UserProvider>
        </StrictMode>
    </Provider>
);
