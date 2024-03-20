import {create} from 'zustand';
import {mountStoreDevtool} from 'simple-zustand-devtools';

// Create a new store called 'useAuthStore' using the 'create function
const useAuthStore = create((set, get) => ({
    //initialize 'allUserData' as 'null' to store all userdata
    allUserData: null,
    loading: false,

    /* Setter funcions
    SetUser: take user object and updates the allUserData in the store
    SetLoading:Take boolean value and update the loading in the store
    
    setLoggedin:Check if user is logged in by verifying 'allUserData
    is not null,returns boolean
    */
    setUser: (user) => set({allUserData: user}),
    setLoading: (loading) => set({loading}),
    setLoggedIn: () => get().allUserData !== null,

    /*getter function
    - function to get user data from store
    - if allUserData is not null get user_id and
    username otherwise set it as 'null'*/
    user: () => ({
        user_id: get().allUserData?.user_id || null,
        username: get().allUserData?.username || null,
    }),

}));

/*check if app is running in dev mode
  then enable 'mountStoreDevtool to visualize and
 interact with the useAuthStore */
if(import.meta.env.DEV) {
    mountStoreDevtool('Store', useAuthStore);
}

export {useAuthStore};