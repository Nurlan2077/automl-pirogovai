function submitData() {
    var id = 1
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
    const xmlHttp = new XMLHttpRequest();
    xmlHttp.open("POST", `http://pirogov-backend.net:8000/user-sessions/${id}/learn`, true);

    xmlHttp.onreadystatechange = function () {
        alert(xmlHttp.readyState)
        if (xmlHttp.readyState === 4) {
            alert("Гиперпараметры были отправлены!");
        }
    }
    alert(JSON.stringify({"params": json_items}))
    xmlHttp.setRequestHeader("Content-Type", "application/json");
    xmlHttp.send(JSON.stringify({"params": json_items}))
}