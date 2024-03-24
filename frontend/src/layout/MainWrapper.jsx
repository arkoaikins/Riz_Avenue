import { useEffect, useState } from "react";
import { setUser } from "../utils/auth"

// Goal is to handle the loading state and perform user auth actions 
// Functional react component "MainWrapper" that wraps children components
const MainWrapper = ({ children }) => {
    // State variable for loading status(initally set to true- indicate loading)
    const [loading, setLoading] = useState(true);

    // useEffect hook to run a side effect when component mounts
    useEffect(() => {
        // Define async handler to set loading,call setUser and reset loading state
        const handler = async () => {
            setLoading(true);
            await setUser(); // call SetUser to perform user authentication
            setLoading(false); // set loading state to false after setUser completes
        }
        //Invoke the handler function(to ensure user Authentication actions are performed when components mount)
        handler();
    }, []); // Empty dependency array to ensure the effect runs only once on mount
    // Render children prop only when loading is false
    return <>{loading ? null : children}</>;
}

export default MainWrapper;