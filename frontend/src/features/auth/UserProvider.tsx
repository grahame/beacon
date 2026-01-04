import { useAppDispatch, useAppSelector } from "../../rtk/hooks";
import { UserBootstrap } from "./Actions";
import { selectUser, type UserState } from "./User";

const UserLoggedIn = (state: UserState): boolean => {
    return state.valid === true && state.user !== undefined;
};

export const UserProvider: React.FC<React.PropsWithChildren<unknown>> = ({ children }) => {
    const dispatch = useAppDispatch();

    dispatch(UserBootstrap());

    const state = useAppSelector(selectUser);

    if (UserLoggedIn(state)) {
        return <div>{children}</div>;
    } else {
        return <div>not logged in...</div>;
    }
};
