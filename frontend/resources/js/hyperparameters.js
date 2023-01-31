function submitData() {
    let url = '';
    let xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            alert("Гиперпараметры были отправлены!");
            window.location.replace = "";
        }
    };

    let formData = new FormData(document.getElementById('hyperparametersForm'))
    for (var pair of formData.entries()) {
        if (pair[0] == "learningRate" && pair[1] == "") formData.set("learningRate", "learn");
        if (pair[0] == "epochs" && pair[1] == "") formData.set("epochs", "epoch");
    }

    xhr.send(formData);
}