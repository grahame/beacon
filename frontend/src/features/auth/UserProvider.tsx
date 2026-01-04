import { useEffect } from "react";
import { Button } from "reactstrap";
import { useAppDispatch, useAppSelector } from "../../rtk/hooks";
import { UserBootstrap } from "./Actions";
import { selectUser, type UserState } from "./User";

const UserLoggedIn = (state: UserState): boolean => {
    return state.valid === true && state.user !== undefined;
};

const SignInButton: React.FC = () => {
    const handleSignIn = async () => {
        const response = await fetch("/api/v1/auth/theolau/authorize");
        const data = await response.json();
        window.location.href = data.authorization_url;
    };

    return <Button onClick={handleSignIn}>Sign in</Button>;
};

export const UserProvider: React.FC<React.PropsWithChildren<unknown>> = ({ children }) => {
    const dispatch = useAppDispatch();
    const state = useAppSelector(selectUser);

    useEffect(() => {
        dispatch(UserBootstrap());
    }, [dispatch]);

    if (UserLoggedIn(state)) {
        return <div>{children}</div>;
    } else {
        return <SignInButton />;
    }
};
