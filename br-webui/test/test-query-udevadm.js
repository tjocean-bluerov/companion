var express = require('express');
var app = express();
var path = require("path");
const child_process = require('child_process');

var _companion_directory = "../.."

var server = app.listen(2770, function() {
    var host = server.address().address;
    var port = server.address().port;
    console.log("App running at http://%s:%s", host, port);
});

app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname + "/test-query-udevadm.html"));
});

app.get("/udevadm", function(req, res) {
    var pattern = "";

    if (req.query.pattern) {
        pattern = "--pattern=" + req.query.pattern;
    }

    console.log("got request for udevadm query:" + req.query.pattern);

	child_process.exec(_companion_directory + "/tools/query-udevadm.py --indent=2 " + pattern, function(error, stdout, stderr) {
		res.setHeader('Content-Type', 'application/json');
		res.send(stdout.toString());
	});
});
