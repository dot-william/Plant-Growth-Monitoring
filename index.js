//Broker
const aedes = require ('aedes');
const server = require('net').createServer(aedes.handle);
const port = 1883;

//Express Server and MySQL 
const express = require('express');
const db = require('./models/db.js');
const dotenv = require('dotenv');
const bodyParser = require('body-parser');
var hostname = "localhost";

// App set-up
const app = express();
app.use(bodyParser.urlencoded({ extended: false }));


// Initialize DB Connection
db.connect();

server.listen(port, function(){
    console.log('server started and listening on port ', port);
});

app.listen(port_app, hostname, ()=> {
    console.log(`Server running at:`);
    console.log('http://' + hostname + ':' + port_app);
});
  