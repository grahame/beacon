import { createSlice } from "@reduxjs/toolkit";
import type { PayloadAction } from "@reduxjs/toolkit";

export interface CounterState {
    valid: boolean;
}

const initialState: CounterState = {
    valid: false,
};

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
