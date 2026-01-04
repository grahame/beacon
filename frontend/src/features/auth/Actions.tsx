import { createAsyncThunk } from "@reduxjs/toolkit";
import type { AxiosRequestConfig } from "axios";
import { deleteJWT, getJwt } from "./jwt";
import axios from "axios";
import type { User } from "./User";

export const ApiAxiosRequestConfig = (): AxiosRequestConfig => {
    const headers: AxiosRequestConfig["headers"] = { "Content-Type": "application/json" };
    const token = getJwt();
    if (token) {
        headers["Authorization"] = token.token_type + " " + token.access_token;
    }
    return {
        headers: headers,
    };
};

const getUser = async () => {
    try {
        const resp = await axios.get<User>("/api/v1/users/me", ApiAxiosRequestConfig());
        return resp.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            if (error.response && error.response.status === 401) {
                // we're not logged in
                return undefined;
            }
        }
        return undefined;
    }
};

export const Logout = createAsyncThunk("user/logout", async () => {
    deleteJWT();
    return {
        success: true,
        user: await getUser(),
    };
});

export const UserBootstrap = createAsyncThunk("user/boostrap", async () => {
    return await getUser();
});
