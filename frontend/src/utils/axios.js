// This is an api instance for interacting with the server
// 'axios library- is a promised-based HTTP client for the browser and Node.js
import axios from 'axios';

// Create a new API instance 
const creatAPIInstance = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/v1/',
    timeout: 5000,

    headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json'
    },
    
});
export default  creatAPIInstance;