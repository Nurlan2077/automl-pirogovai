async function postSessionId() {
    const id = 0;
    let json_item = {
        "dataset_path": "test redirect",
        "data_markup_path": "test redirect",
        "user_id": id
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
}
