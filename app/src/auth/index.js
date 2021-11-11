import React, { useContext, createContext, useState } from "react";

const fakeAuth = {
    isAuthenticated: false,
    signin(cb) {
      fakeAuth.isAuthenticated = true;
      setTimeout(cb, 100); // fake async
    },
    signout(cb) {
      fakeAuth.isAuthenticated = false;
      setTimeout(cb, 100);
    }
};
  
const authContext = createContext();
  
function ProvideAuth({ children }) {
    const auth = useProvideAuth();
    return (
        <authContext.Provider value={auth}>
        {children}
        </authContext.Provider>
    );
}

function useAuth() {
    return useContext(authContext);
}

function useProvideAuth() {
    const [user, setUser] = useState(null);

    const login = cb => {
        return fakeAuth.signin(() => {
        setUser("user");
        cb();
        });
    };

    const logout = cb => {
        return fakeAuth.signout(() => {
        setUser(null);
        cb();
        });
    };

return {
    user,
    login,
    logout
};
}
