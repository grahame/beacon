import { useEffect } from "react";
import { Button, Card, CardBody, CardSubtitle, CardText, CardTitle, Container } from "reactstrap";
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
        <Container>
            <Card className="mb-4">
                <CardBody>
                    <CardTitle tag="h1">Beacon</CardTitle>
                    <CardSubtitle>
                        <em>Emergency alerts for parishes in the Anglican Diocese of Perth</em>
                    </CardSubtitle>
                    <CardText>
                        <p className="fs-5" style={{ paddingTop: "1em" }}>
                            This website is provided as an unofficial service in support of pastoral ministry within the
                            Diocese. Sign in or create an account to subscribe to notifications (sent via email) for
                            warnings posted to Emergency WA that fall within the boundaries of any given parish in the
                            Diocese. This is intended to help clergy and lay leaders offer support to the community when
                            emergencies arise in parishes.
                        </p>
                        <p>
                            <Button color="primary" onClick={handleSignIn}>
                                Sign in or create an account
                            </Button>
                        </p>
                    </CardText>
                </CardBody>
            </Card>

            <p></p>

            <p>
                <img className="img-fluid" src="beacon-landing.png" alt="Parish boundaries" />
            </p>

            <p>
                Any queries can be sent to <a href="mailto:frgrahame@bowland.au">Fr Grahame Bowland</a>.
            </p>
        </Container>
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
