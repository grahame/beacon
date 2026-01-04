import { useEffect } from "react";
import { useSearchParams, useNavigate } from "react-router";
import { storeJwt } from "./jwt";

export const OAuthCallback: React.FC = () => {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();

    useEffect(() => {
        const code = searchParams.get("code");
        const state = searchParams.get("state");

        if (code && state) {
            const params = new URLSearchParams({ code, state });
            fetch(`/api/v1/auth/theolau/callback?${params}`, {
                method: "GET",
            })
                .then((response) => response.json())
                .then((data) => {
                    storeJwt({
                        access_token: data.access_token,
                        token_type: data.token_type,
                    });
                    navigate("/");
                });
        }
    }, [searchParams, navigate]);

    return <div>Processing login...</div>;
};
