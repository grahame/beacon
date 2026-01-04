import "./App.css";
import { useEffect, useState } from "react";
import { Button, Card, CardBody, CardTitle, CardText, Table } from "reactstrap";
import axios from "axios";
import { useAppDispatch, useAppSelector } from "./rtk/hooks";
import { selectUser } from "./features/auth/User";
import { Logout, ApiAxiosRequestConfig } from "./features/auth/Actions";

interface ParishSubscription {
    parish: string;
    subscribed: boolean;
}

const Subscriptions: React.FC = () => {
    const [subscriptions, setSubscriptions] = useState<ParishSubscription[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchSubscriptions = async () => {
            try {
                const resp = await axios.get<ParishSubscription[]>(
                    "/api/v1/subscriptions",
                    ApiAxiosRequestConfig()
                );
                const sorted = [...resp.data].sort((a, b) => {
                    if (a.subscribed !== b.subscribed) {
                        return a.subscribed ? -1 : 1;
                    }
                    return a.parish.localeCompare(b.parish);
                });
                setSubscriptions(sorted);
            } catch (err) {
                setError("Failed to load subscriptions");
            } finally {
                setLoading(false);
            }
        };
        fetchSubscriptions();
    }, []);

    if (loading) {
        return <p>Loading subscriptions...</p>;
    }

    if (error) {
        return <p>{error}</p>;
    }

    return (
        <Table striped>
            <thead>
                <tr>
                    <th>Parish</th>
                    <th>Subscribed</th>
                </tr>
            </thead>
            <tbody>
                {subscriptions.map((sub) => (
                    <tr key={sub.parish}>
                        <td>{sub.parish}</td>
                        <td>{sub.subscribed ? "Yes" : "No"}</td>
                    </tr>
                ))}
            </tbody>
        </Table>
    );
};

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
    return (
        <>
            <UserWelcome />
            <Subscriptions />
        </>
    );
}

export default App;
