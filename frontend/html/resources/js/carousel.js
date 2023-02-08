const id = sessionStorage.getItem("sessionId")
const fetchOptions = {
    method: 'GET'
};
const jsZip = JSZip();
fetch(`http://pirogov-backend.net:8000/user-sessions/${id}/send-archive`, fetchOptions)
    .then(response => response.arrayBuffer())
    .then(arrayBuffer => {
        jsZip.loadAsync(arrayBuffer)
            .then(zip => {
                Object.keys(zip.files).forEach(f_name => {
                    zip.file(f_name).async("arraybuffer").then(function (content) {
                        const blob = new Blob([content], {type: "application/x-hdf"});
                        const link = document.getElementById('download');
                        link.href = URL.createObjectURL(blob);
                        link.download = "model.hdf5";
                    });
                });
            })
    })

const responseElement = document.getElementById('metrics');

const modelId = sessionStorage.getItem("modelId")
fetch(`http://pirogov-backend.net:8000/model-metrics/${modelId}`)
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
            }
            result += `${item.metric_name}: ${item.metric_value}` + newLine
        }
        // Write the response string into the HTML p element
        responseElement.innerText = result;
    })
    .catch(error => {
        // Handle the error
        console.error(error);
        responseElement.innerText = "An error occurred while fetching the data.";
    });
