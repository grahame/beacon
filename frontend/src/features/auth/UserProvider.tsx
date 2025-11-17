import { useAppDispatch } from "../../rtk/hooks";
import { UserBootstrap } from "./Actions";

export const AuthProvider: React.FC<React.PropsWithChildren<unknown>> = ({ children }) => {
    const dispatch = useAppDispatch();

    dispatch(UserBootstrap());

    return <div>{children}</div>;
};
