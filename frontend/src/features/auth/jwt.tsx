export interface IJwt {
    readonly access_token: string;
    readonly token_type: string;
}

export const storeJwt = (jwt: IJwt) => {
    localStorage.setItem("jwt", JSON.stringify(jwt));
};

export const getJwt = (): IJwt | null => {
    const jwt = localStorage.getItem("jwt");
    if (jwt) {
        return JSON.parse(jwt);
    }
    return null;
};

export const deleteJWT = () => {
    localStorage.removeItem("jwt");
};
