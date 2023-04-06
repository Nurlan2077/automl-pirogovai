const userId = sessionStorage.getItem("userId");

// If user_id is undefined, redirect to the login page
if (!userId) {
    window.location.replace("http://0.0.0.0:3000/index");
    alert("Вы не вошли в аккаунт");
}

// Make the GET request
const url = `http://pirogov-backend.net:8000/users/${userId}`;
fetch(url)
    .then(response => {
        if (response.status !== 200) {
            window.location.replace("http://0.0.0.0:3000/index");
            alert("Вы не вошли в аккаунт");
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });