const id = sessionStorage.getItem("sessionId")
const socket = new WebSocket(`ws://pirogov-backend.net:8000/user-sessions/${id}/progress`);

socket.onmessage = function (event) {
    if (event.data === "Processing completed.") {
        alert("Обучение завершено!")
        window.location.replace("http://0.0.0.0:3000/carousel");
    }
    else if (event.data.includes("model id: ")) {
        let id = event.data.substring(event.data.indexOf(":")+2)
        sessionStorage.setItem("modelId", id)
    }
    else {
        console.log(event.data);
        let bar = document.querySelector(".progress-bar");
        bar.style.width = event.data;
        bar.innerText = event.data;
    }
}
