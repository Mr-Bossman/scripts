const express = require('express');
const app = express();
var fs = require('fs');
var ffmpeg = require('fluent-ffmpeg');
var PubSub = require("pubsub-js");
var net = require("net");
var connections = 0
var client = new net.Socket();
const boundaryID = "BOUNDRY";
app.get('/', (req, res, next) => {
    res.sendfile('./index.html');
})

app.get('/vid.jpg', function(req, res) {

    res.writeHead(200, {
        'Content-Type': 'multipart/x-mixed-replace;boundary="' + boundaryID + '"',
        'Connection': 'keep-alive',
        'Expires': 'Fri, 27 May 1977 00:00:00 GMT',
        'Cache-Control': 'no-cache, no-store, max-age=0, must-revalidate',
        'Pragma': 'no-cache'
    });

    var sub = PubSub.subscribe('MJPEG', function(msg, data) {

        //console.log(data.length);

        res.write('--' + boundaryID + '\r\n')
        res.write('Content-Type: image/jpeg\r\n');
        res.write('Content-Length: ' + data.length + '\r\n');
        res.write("\r\n");
        res.write(data, 'binary');
        res.write("\r\n");
    });

    res.on('close', function() {
        PubSub.unsubscribe(sub);
        res.end();
    });
});

function ff() {
    return ffmpeg('/dev/video2').videoBitrate('1024k').addInputOption("-re").outputFormat("mjpeg").fps(15).size('1080x720').addOptions("-q:v 10");
}
var command = ff();
var ffstream = command.pipe();
ffstream.on('data', function(chunk) {
    PubSub.publish('MJPEG', chunk);
});

function restart() {
    ffstream.destroy();
    command.kill();
    command = ff();
    ffstream = command.pipe();
    ffstream.on('data', function(chunk) {
        PubSub.publish('MJPEG', chunk);
    });
    ffstream.on("end", restart);
}
ffstream.on("end", restart);
app.listen(8080);