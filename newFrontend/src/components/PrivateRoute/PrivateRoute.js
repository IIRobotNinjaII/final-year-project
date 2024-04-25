import { Navigate } from "react-router-dom";

const PrivateRoute = ({ conditional, element, fallback }) => {
    return conditional ? element : <Navigate to={fallback} />
}

export default PrivateRoute;