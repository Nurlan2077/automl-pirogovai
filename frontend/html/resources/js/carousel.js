const id = sessionStorage.getItem("sessionId")
const fetchOptions = {
    method: 'GET'
};
const jsZip = JSZip();
fetch(`http://pirogov-backend.net:8000/user-sessions/${id}/send-archive`, fetchOptions)
    .then(response => response.blob())
    .then(blob => {
        const link = document.getElementById('download');
        link.href = URL.createObjectURL(blob);
        link.download = "archive.zip";
        link.style.display = "block";
    });

const responseElement = document.getElementById('metrics');
const modelId = sessionStorage.getItem("modelId")
fetch(`http://pirogov-backend.net:8000/model-metrics/with-names/${modelId}`)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        let result = ""
        let modelName = ""
        let newLine;

        if (navigator.platform.indexOf("Win") === 0) {
            newLine = "\r\n";
        } else {
            newLine = "\n";
        }
        for (let i = 0; i < data.length; i++) {
            let item = data[i]
            if (i === 0) {
                modelName = item.model_name
                document.getElementById('modelName').innerText = modelName;
            }
            result += `${item.metric_name}: ${item.metric_value}` + newLine
        }
        // Write the response string into the HTML p element
        responseElement.innerText = result;
    })
    .catch(error => {
        // Handle the error
        console.error(error);
        responseElement.innerText = "Произошла ошибка при загрузке результата. Попробуйте позднее";
    });
