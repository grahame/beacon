import { createSlice } from "@reduxjs/toolkit";
import type { PayloadAction } from "@reduxjs/toolkit";

export interface CounterState {
    valid: boolean;
}

const initialState: CounterState = {
    valid: false,
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
export default userSlice.reducer;
