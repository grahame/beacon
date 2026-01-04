import { createSlice } from "@reduxjs/toolkit";
import type { PayloadAction } from "@reduxjs/toolkit";
import type { RootState } from "../../rtk/store";

export interface UserState {
    // have we bootstrapped the user process?
    readonly valid: boolean;
    // if the user is undefined, we are not logged in
    readonly user: User | undefined;
}

const initialState: UserState = {
    valid: false,
    user: undefined,
};

export interface User {
    readonly email: string;
    readonly is_active?: boolean;
    readonly is_superuser?: boolean;
    readonly is_verified?: boolean;
    readonly password?: string;
    readonly name: string;
    readonly affiliation?: string;
}

export const userSlice = createSlice({
    name: "user",
    initialState,
    reducers: {
        setValid: (state, action: PayloadAction<boolean>) => {
            state.valid = action.payload;
        },
    },
});

// Action creators are generated for each case reducer function
export const { setValid } = userSlice.actions;
export const selectUser = (state: RootState) => state.user;
export default userSlice.reducer;
