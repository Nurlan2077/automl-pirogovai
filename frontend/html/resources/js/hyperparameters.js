function is_default(val) {
    return val.toLowerCase() === "default"
}

function submitData() {
    const id = sessionStorage.getItem('sessionId');
    let formData = new FormData(document.getElementById('hyperparametersForm'));
    let json_items = {}
    for (const pair of formData.entries()) {
        switch (pair[0]) {
            case "epochs":
                json_items[pair[0]] = parseInt(pair[1].toString())
                break
            case "optimizer":
                if (!(pair[0] in json_items)) json_items[pair[0]] = []
                    json_items[pair[0]].push(pair[1])
                break
            case "lossFunction":
                if (!(pair[0] in json_items)) json_items[pair[0]] = []
                    json_items[pair[0]].push(pair[1])
                break
        }
    }
    const fetchOptions = {
        method: 'POST', body: JSON.stringify(json_items), headers: {
            'Content-Type': 'application/json '
        }
    };

    fetch(`http://pirogov-backend.net:8000/user-sessions/${id}/hyperparams`, fetchOptions)
        .then(response => {
            alert("Гиперпараметры были отправлены!")
            window.location.replace("http://0.0.0.0:3000/progress-bar")
        });
}