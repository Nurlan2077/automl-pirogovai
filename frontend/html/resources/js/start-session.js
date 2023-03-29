async function postSessionId() {
    const id = sessionStorage.getItem("userId");
    let json_item = {
        "dataset_path": "",
        "data_markup_path": "",
        "model_path": "",
        "user_id": id,
        "metrics_path": ""
    }
    const fetchOptions = {
        method: 'POST', body: JSON.stringify(json_item ), headers: {
            'Content-Type': 'application/json '
        }
    };

    let response = await fetch(`http://pirogov-backend.net:8000/user-sessions/`, fetchOptions);
    let result = await response.json();
    if (response.status === 201) {
        sessionStorage.setItem("sessionId", result.id);
        window.location.replace("http://0.0.0.0:3000/data-upload");
    }
    else alert("Не удалось начать новую сессию. Повторите попытку позже")
}
