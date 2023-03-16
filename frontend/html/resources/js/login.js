function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const loginUrl = "https://auth.pirogov.ai/remote_login";
    const authenticateUrl = "http://pirogov-backend.net:8000/users/authenticate";

    // Make the first POST request
    fetch(loginUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            key: 0,
            login: email,
            password: password
        })
    })
        .then(response => {
            if (response.status !== 200) {
                throw new Error('Authentication failed');
            }
            return response.json();
        })
        .then(result => {
            // Make the second POST request
            return fetch(authenticateUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    id: result.user_id,
                    name: result.user_info.name,
                    email: result.user_info.email
                })
            });
        })
        .then(response => {
            if (response.status === 200) {
                sessionStorage.setItem('user_id', response.json().user_id);
                alert("Вход успешен!")
                window.location.replace("http://0.0.0.0:3000/start-session")
            } else {
                throw new Error('Authentication failed');
            }
        })
        .catch(error => {
            alert(error.message);
        });
}