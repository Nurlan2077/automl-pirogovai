const http = require('http');
const fs = require('fs');
const path = require("path");

const hostname = '0.0.0.0';
const port = 3000;

const server = http.createServer((req, response) => {
    console.log(`Serving request for ${req.url}`);
    const extname = path.extname(req.url);
    if (extname !== '.js' && extname !== '.css') {
        let filePath = `./html${req.url === '/' ? '/index.html' : req.url}`;
        if (!filePath.endsWith(".html"))
            filePath += ".html";
        fs.readFile(filePath, (error, data) => {
            if (error) {
                console.error(`Error reading file: ${error}`);
                response.writeHead(404, {'Content-Type': 'text/plain'});
                response.end('File not found');
            } else {
                response.writeHead(200, {'Content-Type': 'text/html'});
                response.end(data);
            }
        });
    } else {
        response.writeHead(200, {'Content-Type': 'text/html'});
        response.end();
    }
});

server.listen(port, hostname, (error) => {
    if (error) console.error(`Error: ${error}`)
    else console.log(`Server running at http://${hostname}:${port}`);
});