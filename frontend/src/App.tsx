import "./App.css";
import { useEffect, useState } from "react";
import { Button, Card, CardBody, CardTitle, CardText, Table } from "reactstrap";
import axios from "axios";
import { useAppDispatch, useAppSelector } from "./rtk/hooks";
import { selectUser } from "./features/auth/User";
import { Logout, ApiAxiosRequestConfig } from "./features/auth/Actions";

interface ParishSubscription {
    parish_id: number;
    parish: string;
    subscribed: boolean;
}

const sortSubscriptions = (data: ParishSubscription[]) => {
    return [...data].sort((a, b) => {
        if (a.subscribed !== b.subscribed) {
            return a.subscribed ? -1 : 1;
        }
        return a.parish.localeCompare(b.parish);
    });
};

const Subscriptions: React.FC = () => {
    const [subscriptions, setSubscriptions] = useState<ParishSubscription[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchSubscriptions = async () => {
        try {
            const resp = await axios.get<ParishSubscription[]>("/api/v1/subscriptions", ApiAxiosRequestConfig());
            setSubscriptions(sortSubscriptions(resp.data));
        } catch {
            setError("Failed to load subscriptions");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchSubscriptions();
    }, []);

    const handleSubscribe = async (parishId: number) => {
        await axios.post("/api/v1/subscribe", { parish_id: parishId }, ApiAxiosRequestConfig());
        await fetchSubscriptions();
    };

    const handleUnsubscribe = async (parishId: number) => {
        await axios.post("/api/v1/unsubscribe", { parish_id: parishId }, ApiAxiosRequestConfig());
        await fetchSubscriptions();
    };

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
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                {subscriptions.map((sub) => (
                    <tr key={sub.parish_id}>
                        <td>{sub.parish}</td>
                        <td>{sub.subscribed ? "Yes" : "No"}</td>
                        <td>
                            {sub.subscribed ? (
                                <Button color="danger" size="sm" onClick={() => handleUnsubscribe(sub.parish_id)}>
                                    Unsubscribe
                                </Button>
                            ) : (
                                <Button color="primary" size="sm" onClick={() => handleSubscribe(sub.parish_id)}>
                                    Subscribe
                                </Button>
                            )}
                        </td>
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
                <CardText>
                    <p>Logged in as {user.email}.</p>
                    <p>
                        For each parish within the Anglican Diocese of Perth, you can subscribe to receive notifications
                        (sent via email) for any warning posted to Emergency WA that falls within the boundaries of that
                        parish.
                    </p>
                    <p>
                        This service is to support of pastoral ministry only, and should not be relied upon for your
                        safety or the safety of others. This is an unofficial service. Any queries can be sent to{" "}
                        <a href="mailto:frgrahame@bowland.au">Fr Grahame Bowland</a>.
                    </p>
                </CardText>
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
