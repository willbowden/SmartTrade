
function protectedFetch(url, args={}){
    return new Promise((resolve, reject) => {
        const token_header = JSON.parse(localStorage.getItem('REACT_TOKEN_AUTH_KEY'));
        try {
            const token = token_header.access_token
            args.headers = {'Authorization': 'JWT ' + token, 'Content-Type': 'application/json'}
            fetch(url, args).then(res => res.json()).then( data => {
                if (data.status_code === 401 || data.status_code === 500) {
                    reject(data)
                } else {
                    resolve(data)
                }
            })
        } catch(err) {
            reject()
        }
    })
}

export default protectedFetch;