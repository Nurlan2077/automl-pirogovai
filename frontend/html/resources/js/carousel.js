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
                        link.download = "model.h5";
                    });
                });
            })
    })

