//Broker
const aedes = require ('aedes');
const server = require('net').createServer(aedes.handle);
const port = 1883;

//Express Server and MySQL 
const express = require('express');
const db = require('./models/db.js');
const helper  = require('./helperFunction');
const dotenv = require('dotenv');
const bodyParser = require('body-parser');
var hostname = "localhost";

// App set-up
const app = express();

//Valid topics and type to check
const validTopics = ["sensor", "dlsu", "node-1"]
const validTopicTypes = ["lightintensity", "temperature", "humidity", "soilmoisture", "ph", "images"]

// DB variables
const db_name = `pgmsdb`;
const experiment = `cherrytomato`;
const address = `dlsu`;
const node = `sensornode`;
const location = address + '_' + experiment + '_' + node;

app.use(bodyParser.urlencoded({ extended: false }));


// Initialize DB Connection
db.connect();

server.listen(port, function(){
    console.log('server started and listening on port ', port);
});

app.listen(port_app, hostname, () => {
    console.log(`Server running at:`);
    console.log('http://' + hostname + ':' + port_app);
});

// Broker
aedes.on('publish', async function(packet, client) {
    isValidTopic = helper.checkTopic(packet.topic, validTopics, validTopicTypes);
    
    if(client && isValidTopic) {
        if(!packet.topic.includes("images")) {
            var raw_data = JSON.parse(packet.payload.toString());
            
        } else
            helper.logMessage("Image saved locally.");
        


    } else if (client && !isValidTopic) {
        let errorMsg = "Packet format incorrect. Length not at least 4.";
        let errorLog = helper.errorLog(errorMsg);
        helper.logMessage(errorMsg);
        db.insertTable(msg, "error_msg");
    }
});