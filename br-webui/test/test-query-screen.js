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
    res.sendFile(path.join(__dirname + "/test-query-screen.html"));
});

app.get("/screen", function(req, res) {
    var user = "";

    if (req.query.user) {
        user = "--user=" + req.query.user;
    }

    console.log("got request for screens on user:" + req.query.user);

	child_process.exec(_companion_directory + "/tools/query-screen.py --indent=2 " + user, function(error, stdout, stderr) {
		res.setHeader('Content-Type', 'application/json');
		res.send(stdout.toString());
	});
});
