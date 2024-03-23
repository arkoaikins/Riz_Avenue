import {useAuthStore} from '../store/auth';
import axios from './axios';
import jwt_decode from 'jwt-decode';
import Cookies from 'js-cookie';

// Function for user login with axios to post user credentials  
export const login = async (email, password) => {
    try{
        // send POST request to endpoint with email and password
        const {data, status} = await axios.post("user/token/", {
            email,
            password

        });
        // If request is sucess(status code 200)
        if (status === 200) {
            // Set authentication user using access and refresh tokens obtained
            setAuthUser(data.access, data.refresh);
            
            //add alerts(to be done)
        }
        // return the response data and no error
        return {data, error: null};
    } catch (error) {
        // if error occurs return error and no data
        return {
            data: null,
            error: error.response.data?.detail || 'Something went wrong',
        };

    }
};

// Function to  user registeration with axios to post user credentials
export const register = async(full_name, email, phone, password, password2) => {
    try {
        // send POST request to endpoint with registeration data
        const {data} = await axios.post('user/register/', {
            full_name, email, phone, password, password2,
        });
        // logging in the user after successful registeration
        await login(email, password);
        
        // add login alert(to be done)

        // If all is sucess return response data and no error
        return {data, error: null}
    } catch(error) {
        // if an error occurs return error and no data
        return {
            data: null,
            error: error.response.data.detail || 'Something went wrong',
        };
    }
};

// Function for user logout
export const logout = () => {
    // Remove acess and refresh token
    Cookies.remove("access_token");
    Cookies.remove("refresh_token");
    // and set the user in the authentication store to null
    useAuthStore.getState().setUser(null);

    //display logout alrert(to be done)
};

// Function to set the user in the authentication store
export const setUser = async () => {
    // Get access and refresh token from Cookiess
    const accessToken = Cookies.get("access_token")
    const refreshToken = Cookies.get("refresh_token")

    // if no access or refresh token, return
    if(!accessToken || !refreshToken) {
        return;
    }
    // if acess token is expired we obtain new tokens using the getRefresh token func
    if (isAccessTokenExpired(accessToken)) {
        const response = await getRefreshToken(refreshToken);
        setAuthUser(response.access, response.refresh);
    } else {
        // otherwise set the user using the existing tokens
        setAuthUser(accessToken, refreshToken);
    }
};

// Function to set authenticated user in the AuthStore
export const setAuthUser = (access_token, refresh_token) => {
    // set access token Cookies to expire after 1 day with a secure flag
    Cookies.set('access_token', access_token, {
        expire: 1,
        secure: true,
    });

    // set refresh token Cookies to expire after a week with a secure flag
    Cookies.set('refresh_token', refresh_token, {
        expire: 7,
        secure: true,
    });

    // Decode access token to get user data
    const user = jwt_decode(access_token) ?? null;
    
    // Set user in the authentication store
    if (user) {
        useAuthStore.getState().setUser(user);
    }
    // set loading state to false to ensure that all process are done
    useAuthStore.getState().setLoading(false);
};

// Function to obtain new acess and refresh token from the backend by POST request with axios
export const getRefreshToken = async () => {
    // get the unexpired refresh token from the Cookies
    const refresh_token = Cookies.get("refresh_token");
    // send POST request to the endpoint with refresh token
    const response = await axios.post("user/token/refresh/", {
        refresh: refresh_token,
    });
    // Return the new generated refresh and access token
    return response.data;
};

// Function to check if the access token is expired
export const isAccessTokenExpired = (accessToken) => {
    try {
        // decode the access token
        const decodedToken = jwt_decode(accessToken);
        // check if the token expiration time is earlier than the current time
        return decodedToken.exp < Date.now() / 1000;
    } catch (error) {
        console.log(error)
        return true
    }
};