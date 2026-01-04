import { useEffect } from "react";
import { Button } from "reactstrap";
import { useAppDispatch, useAppSelector } from "../../rtk/hooks";
import { UserBootstrap } from "./Actions";
import { selectUser, type UserState } from "./User";

const UserLoggedIn = (state: UserState): boolean => {
    return state.valid === true && state.user !== undefined;
};

const SignIn: React.FC = () => {
    const handleSignIn = async () => {
        const response = await fetch("/api/v1/auth/theolau/authorize");
        const data = await response.json();
        window.location.href = data.authorization_url;
    };

    return (
        <>
            <h2>Beacon: emergency alerts for parishes in the Anglican Diocese of Perth</h2>

            <p>
                This website is provided as an unofficial service in support of pastoral ministry within the Diocese.
                Sign in or create an account to subscribe to notifications (sent via email) for any warning posted to
                Emergency WA that falls within the boundaries of any parish in the Diocese.
            </p>
            <p>
                This is intended to help clergy and lay leaders offer support to the community when emergencies arise in
                parishes.
            </p>
            <p>
                Any queries can be sent to <a href="mailto:frgrahame@bowland.au">Fr Grahame Bowland</a>.
            </p>

            <Button onClick={handleSignIn}>Sign in or create an account</Button>
        </>
    );
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
        return <SignIn />;
    }
};
