function protectedFetch(url, ...rest){
    return new Promise((resolve, reject) => {
        const token_header = JSON.parse(localStorage.getItem('REACT_TOKEN_AUTH_KEY'));
        const token = token_header.access_token
        fetch(url, {headers: {'Authorization': 'JWT ' + token, ...rest}}).then(res => res.json()).then( data => {
            resolve(data);
        })
    })
}

export default protectedFetch;