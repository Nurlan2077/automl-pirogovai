async function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    /* TODO:
        change loginUrl to https://auth.pirogov.ai/remote_login when this service will be available
     */
    const loginUrl = "http://pirogov-backend.net:8000/users/login";
    const authenticateUrl = "http://pirogov-backend.net:8000/users/authenticate";

    // Make the first POST request
    await fetch(loginUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            /* TODO:
                change key when login service will be available
             */
            key: 0,
            login: email,
            password: password
        })
    })
        .then(response => {
            if (response.status !== 200) {
                throw new Error('Ошибка аутентификации! Проверьте правильность введенных данных');
            }
            return response.json();
        })
        .then(async result => {
            // Make the second POST request
            return await fetch(authenticateUrl, {
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
        .then(async response => {
            if (response.status === 200) {
                id = (await response.json()).id
                sessionStorage.setItem('userId', id);
                alert("Вход успешен!")
                window.location.replace("http://0.0.0.0:3000/start-session")
            } else {
                throw new Error('Ошибка аутентификации! Проверьте правильность введенных данных');
            }
        })
        .catch(error => {
            alert(error.message);
        });
}