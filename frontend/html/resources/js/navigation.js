let navigation = `
<nav class="navbar fixed-top navbar-expand-lg navbar-dark p-md-3 mask-custom shadow-0">
    <div class="container">
        <a class="navbar-brand">PirogovAI</a>
        <div class="collapse navbar-collapse" id="navbarNav">
            <div class="mx-auto"></div>
            <ul class="navbar-nav">
`
if (window.location.pathname == "/carousel") {
    navigation +=
        `
                <li class="nav-item">
                    <button type="button" class="btn btn-outline-light btn-rounded" onclick="redirectStartSession()">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                            class="bi bi-arrow-90deg-left" viewBox="0 0 16 16">
                            <path fill-rule="evenodd"
                                d="M1.146 4.854a.5.5 0 0 1 0-.708l4-4a.5.5 0 1 1 .708.708L2.707 4H12.5A2.5 2.5 0 0 1 15 6.5v8a.5.5 0 0 1-1 0v-8A1.5 1.5 0 0 0 12.5 5H2.707l3.147 3.146a.5.5 0 1 1-.708.708l-4-4z" />
                        </svg>
                        Создать новую сессию
                    </button>
                </li>
                `
}

navigation +=
    `
                <li class="nav-item">
                    <button type="button" class="btn btn-outline-light btn-rounded" onclick="logout()">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                            class="bi bi-box-arrow-in-right" viewBox="0 0 16 16">
                            <path fill-rule="evenodd"
                                d="M6 3.5a.5.5 0 0 1 .5-.5h8a.5.5 0 0 1 .5.5v9a.5.5 0 0 1-.5.5h-8a.5.5 0 0 1-.5-.5v-2a.5.5 0 0 0-1 0v2A1.5 1.5 0 0 0 6.5 14h8a1.5 1.5 0 0 0 1.5-1.5v-9A1.5 1.5 0 0 0 14.5 2h-8A1.5 1.5 0 0 0 5 3.5v2a.5.5 0 0 0 1 0v-2z">
                            </path>
                            <path fill-rule="evenodd"
                                d="M11.854 8.354a.5.5 0 0 0 0-.708l-3-3a.5.5 0 1 0-.708.708L10.293 7.5H1.5a.5.5 0 0 0 0 1h8.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3z">
                            </path>
                        </svg>
                        Выйти
                    </button>
                </li>
            </ul>
        </div>
    </div>
</nav>
`
document.body.insertAdjacentHTML("afterbegin", navigation)

function logout() {
    sessionStorage.clear();
    alert("Вы вышли из аккаунта");
    window.location.replace("http://0.0.0.0:3000/index");
}

function redirectStartSession() {
    const userId = sessionStorage.getItem("userId");
    sessionStorage.clear();
    sessionStorage.setItem('userId', userId);
    alert("Вы можете начать новую сессию!");
    window.location.replace("http://0.0.0.0:3000/start-session");
}