import axios from "axios";
import { isAccessTokenExpired, setAuthUser, getRefreshToken } from "./auth";
import { BASE_URL } from "./constants";
import Cookies from "js-cookie";

// function to create and configure an Axios instance
const useAxios = async () => {
    // Get access and refresh token from cookie
    const access_token = Cookies.get("access_token")
    const refresh_token = Cookies.get("refresh_token")

    // Create an Axios instance with base URL and  authorization header set
    const axiosInstance = axios.create({
        baseURL: BASE_URL,
        headers: {Authorization: `Bearer ${access_token}`}
    })

    // add Intercepters to handle token expiration and refresh
    axiosInstance.interceptors.request.use(async (req) => {
        // if token is NOT expired return,proceed with request
        if (!isAccessTokenExpired(access_token)) {
            return req
        }
        // if expired,get new tokens using the refresh token
        const response = await getRefreshToken(refresh_token)
        setAuthUser(response.access, response.refresh)

        // Update authorization header with new access token
        req.headers.Authorization = `Bearer ${response.data.access}`
        return req

    })
    // Return the configured Axios instance
    return axiosInstance
    

}

export default useAxios