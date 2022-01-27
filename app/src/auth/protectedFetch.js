function protectedFetch(url, args={}){
    return new Promise((resolve, reject) => {
        const token_header = JSON.parse(localStorage.getItem('REACT_TOKEN_AUTH_KEY'));
        try {
            const token = token_header.access_token
            args.headers = {'Authorization': 'JWT ' + token, 'Content-Type': 'application/json'}
            fetch(url, args).then(res => res.json()).then( data => {
                resolve(data);
            })
        } catch(err) {
            console.log(err)
            resolve({response: "Error"})
        }
    })
}

export default protectedFetch;