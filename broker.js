//Broker
const aedes = require ('aedes')();
const server = require('net').createServer(aedes.handle);
const port = 1883;

//Express Server and MySQL 
const express = require('express');
const db = require('./models/db.js');
const helper  = require('./helperFunction');
const dotenv = require('dotenv');
const bodyParser = require('body-parser');
const ba = require('binascii');
const fs = require('fs');

// App set-up
const app = express();
var hostname = "localhost";
var port_app = 8080;

//Valid topics and type to check
const validTopics = ["sensor", "dlsu", "node-1"]
const validTopicTypes = ["lightintensity", "temperature", "humidity", "soilmoisture", "ph", "images"]

// DB variables
const db_name = `pgmsdb`;

// Table Name for Database
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



// Broker
aedes.on('publish', async function(packet, client) {
    var isValidTopic = helper.checkTopic(packet.topic, validTopics, validTopicTypes);
    
    if(client && isValidTopic) {
        let errorMsg, errorLog;
        var raw_data;
        let parsedData;  
        if(!packet.topic.includes("images")) {
            raw_data = JSON.parse(packet.payload.toString());
            parsedData = helper.parseData(raw_data);
            if(parsedData != null) {
                if(!helper.hasNan(parsedData)) {
                    db.enterData(parsedData, db_name, location);
                } else {
                    errorMsg = "Data does not follow correct packet format.";
                    errorLog = helper.errorLog(errorMsg);
                    helper.logMessage(errorMsg);
                    db.insertTable(errorLog, "error_msg");
                }
            } else {
                errorMsg = "Packet format incorrect.";
                errorLog = helper.errorLog(errorMsg);
                helper.logMessage(errorMsg);
                db.insertTable(errorLog, "error_msg");
            }
        } else
            // When image is published
            raw_data = JSON.parse(packet.payload.toString());
            
            var filename = raw_data["filename"];
            console.log(filename);
            //console.log(raw_data);
            //var img = ba.a2b_base64(raw_data["image_data"]);
            var img = Buffer.from(raw_data["image_data"], 'base64')
            var dest = '/home/student/Plant_Images/Raw/' + filename;
            console.log("Saving to: " + dest);
            fs.writeFile(dest, img, function (err) {
                if(err) throw err;
                helper.logMessage("Image saved locally.");
            })
            
    } else if (client && !isValidTopic) {
        errorMsg = "Invalid topic.";
        errorLog = helper.errorLog(errorMsg);
        helper.logMessage(errorMsg);
        db.insertTable(errorLog, "error_msg");
    }
});

app.listen(port_app, hostname, () => {
    console.log(`Server running at:`);
    console.log('http://' + hostname + ':' + port_app);
});