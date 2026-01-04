import "./App.css";
import { Button, Card, CardBody, CardTitle, CardText } from "reactstrap";
import { useAppDispatch, useAppSelector } from "./rtk/hooks";
import { selectUser } from "./features/auth/User";
import { Logout } from "./features/auth/Actions";

const UserWelcome: React.FC = () => {
    const dispatch = useAppDispatch();
    const state = useAppSelector(selectUser);
    const user = state.user;

    const handleLogout = () => {
        dispatch(Logout());
    };

    if (!user) {
        return null;
    }

    return (
        <Card className="mb-4">
            <CardBody>
                <CardTitle tag="h5">Welcome, {user.name}!</CardTitle>
                <CardText>Logged in as {user.email}</CardText>
                <Button color="danger" onClick={handleLogout}>
                    Log out
                </Button>
            </CardBody>
        </Card>
    );
};

function App() {
    return <UserWelcome />;
}

export default App;
