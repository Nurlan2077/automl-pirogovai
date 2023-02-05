function submitData() {
    const id = 1;
    let formData = new FormData(document.getElementById('hyperparametersForm'));
    let json_items = []
    for (const pair of formData.entries()) {
        let json_pair;
        if (pair[0] === "learningRate" && pair[1] === "") json_pair = {"name": pair[0], "value": "1"};
        else if (pair[0] === "epochs" && pair[1] === "") json_pair = {"name": pair[0], "value": "1"};
        else {
            json_pair = {"name": pair[0], "value": pair[1]};
        }
        json_items.push(json_pair)
    }
    const fetchOptions = {
        method: 'POST', body: JSON.stringify({"params": json_items}), headers: {
            'Content-Type': 'application/json '
        }
    };

    fetch(`http://pirogov-backend.net:8000/user-sessions/${id}/learn`, fetchOptions)
        .then(response => alert("Гиперпараметры были отправлены!"));
}