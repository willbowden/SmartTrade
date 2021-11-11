import {createAuthProvider} from 'react-token-auth';


export const {useAuth, authFetch, login, logout} =
    createAuthProvider({
        getAccessToken: session => session.access_token,
        storage: localStorage,
        accessTokenKey: 'access_token'
});
