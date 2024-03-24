import { Navigate } from 'react-router-dom';
import {useAuthStore} from '../store/auth';

// Functional react component that conditionally renders children based on authentication status
const PrivateRoute = ({ children }) => {
    // Retrieve authentication status from auth store
    const loggedIn = useAuthStore((state) => state.isLoggedIN)();

    // Render children components if user is logged in,otherwise redirect to login page
    return loggedIn ? <>{children}</> : <Navigate to={"/login"} />;
};

export default PrivateRoute;