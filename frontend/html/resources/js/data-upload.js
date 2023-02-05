// ************************ Drag and drop ***************** //
let dropAreaRAR = document.getElementById("drop-area-rar")

    // Prevent default drag behaviors
;['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropAreaRAR.addEventListener(eventName, preventDefaults, false)
    document.body.addEventListener(eventName, preventDefaults, false)
})

// Highlight drop area when item is dragged over it
;['dragenter', 'dragover'].forEach(eventName => {
    dropAreaRAR.addEventListener(eventName, highlightRAR, false)
})

;['dragleave', 'drop'].forEach(eventName => {
    dropAreaRAR.addEventListener(eventName, unhighlightRAR, false)
})

let dropAreaJSON = document.getElementById("drop-area-json")

    // Prevent default drag behaviors
;['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropAreaJSON.addEventListener(eventName, preventDefaults, false)
    document.body.addEventListener(eventName, preventDefaults, false)
})

// Highlight drop area when item is dragged over it
;['dragenter', 'dragover'].forEach(eventName => {
    dropAreaJSON.addEventListener(eventName, highlightJSON, false)
})

;['dragleave', 'drop'].forEach(eventName => {
    dropAreaJSON.addEventListener(eventName, unhighlightJSON, false)
})

// Handle dropped files
dropAreaRAR.addEventListener('drop', handleDropRAR, false)
dropAreaJSON.addEventListener('drop', handleDropJSON, false)

function preventDefaults(e) {
    e.preventDefault()
    e.stopPropagation()
}

function highlightRAR(e) {
    dropAreaRAR.classList.add('highlight')
}

function unhighlightRAR(e) {
    dropAreaRAR.classList.remove('highlight')
}

function highlightJSON(e) {
    dropAreaJSON.classList.add('highlight')
}

function unhighlightJSON(e) {
    dropAreaJSON.classList.remove('highlight')
}

var fileRAR = null
var fileJSON = null
let uploadProgressRAR = []
let uploadProgressJSON = []
let progressBarRAR = document.getElementById('progress-bar-rar')
let progressBarJSON = document.getElementById('progress-bar-json')
let rarSucceed = false
let jsonSucceed = false

function handleRAR(files) {
    let extension = files[0].name.split('.').pop()
    if (extension === "rar") {
        fileRAR = files
        document.getElementById("fileNameRAR").innerHTML = "Файл для загрузки: " + fileRAR[0].name
    } else alert("Неправильный формат!")
}

function handleJSON(files) {
    let extension = files[0].name.split('.').pop()
    if (extension === "PirogovJSON") {
        fileJSON = files
        document.getElementById("fileNameJSON").innerHTML = "Файл для загрузки: " + fileJSON[0].name
    } else alert("Неправильный формат!")
}

function handleDropRAR(e) {
    var dt = e.dataTransfer
    let extension = dt.files[0].name.split('.').pop()
    if (extension === "rar") {
        fileRAR = dt.files
        document.getElementById("fileNameRAR").innerHTML = "Файл для загрузки: " + fileRAR[0].name
    } else alert("Неправильный формат!")
}

function handleDropJSON(e) {
    const dt = e.dataTransfer;
    let extension = dt.files[0].name.split('.').pop()
    if (extension === "PirogovJSON") {
        fileJSON = dt.files
        document.getElementById("fileNameJSON").innerHTML = "Файл для загрузки: " + fileJSON[0].name
    } else alert("Неправильный формат!")
}

function initializeProgress(numFiles, uploadProgress, progressBar) {
    progressBar.value = 0
    uploadProgress = []

    for (let i = numFiles; i > 0; i--) {
        uploadProgress.push(0)
    }
    return [uploadProgress, progressBar]
}

function updateProgress(fileNumber, percent, uploadProgress, progressBar) {
    uploadProgress[fileNumber] = percent
    progressBar.value = uploadProgress.reduce((tot, curr) => tot + curr, 0) / uploadProgress.length
}

function submit() {
    jsonSucceed = false
    rarSucceed = false
    fileRAR = [...fileRAR]
    progressBarRAR = document.getElementById('progress-bar-rar')
    let temp = initializeProgress(fileRAR.length, uploadProgressRAR, progressBarRAR)
    uploadProgressRAR = temp[0]
    progressBarRAR = temp[1]
    fileRAR.forEach((item, index) => uploadFile(item, index, 'upload_dataset', uploadProgressRAR, progressBarRAR, "successRAR"))

    fileJSON = [...fileJSON]
    progressBarJSON = document.getElementById('progress-bar-json')
    temp = initializeProgress(fileJSON.length, uploadProgressJSON, progressBarJSON)
    uploadProgressJSON = temp[0]
    progressBarJSON = temp[1]
    fileJSON.forEach((item, index) => uploadFile(item, index, 'upload_markup', uploadProgressJSON, progressBarJSON, "successJSON"))
}

function uploadFile(file, i, path, uploadProgress, progressBar, type) {
    const id = sessionStorage.getItem('sessionId');
    const url = `http://pirogov-backend.net:8000/user-sessions/${id}/${path}`;
    const xhr = new XMLHttpRequest();
    const formData = new FormData();
    formData.append('file', file)

    xhr.open('POST', url, true)

    // Update progress (can be used to show progress indicator)
    xhr.upload.addEventListener("progress", function (e) {
        updateProgress(i, (e.loaded * 100.0 / e.total) || 100, uploadProgress, progressBar)
    })

    xhr.addEventListener('readystatechange', function (e) {
        if (xhr.readyState === 4 && xhr.status === 200) {
            updateProgress(i, 100, uploadProgress, progressBar)
            document.getElementById(type).innerHTML = "Успешно загружено!";
            if (path === 'upload_dataset') rarSucceed = true
            else if (path === 'upload_markup') jsonSucceed = true
            if (rarSucceed && jsonSucceed) {
                window.location.replace("http://0.0.0.0:3000/hyperparameters")
            }
        } else if (xhr.readyState === 4 && xhr.status !== 200) {
            alert("Ошибка загрузки на сервер! Перезагрузите страницу!")
        }
    })

    xhr.send(formData)
}