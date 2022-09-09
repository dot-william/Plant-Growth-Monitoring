//Broker
const aedes = require ('aedes');
const server = require('net').createServer(aedes.handle);
const port = 1883;

//Express Server and MySQL 
const express = require('express');
//const db = require('./models/db.js');
const helper  = require('./helperFunction');
const dotenv = require('dotenv');
const bodyParser = require('body-parser');
var hostname = "localhost";
var port_app = 8080;
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


// // Initialize DB Connection
// db.connect();

// server.listen(port, function(){
//     console.log('server started and listening on port ', port);
// });

// Create connection https://pimylifeup.com/raspberry-pi-mysql/
const db = mysql.createConnection({
    host : 'localhost',
    user: 'blast',
    password: 'shift12345',
    database: 'shiftdb'
  });
  
  //Connect 
  db.connect(function(err){
    if(err){
      displayError("An error has occured when trying to connect to db.");
      throw err;
    }
    console.log("MySQL Connected...");
  });
  
  server.listen(port, function(){
    console.log('server started and listening on port ', port)
  })



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
            helper.logMessage("Image saved locally.");
    } else if (client && !isValidTopic) {
        errorMsg = "Packet format incorrect. Length not at least 4.";
        errorLog = helper.errorLog(errorMsg);
        helper.logMessage(errorMsg);
        db.insertTable(errorLog, "error_msg");
    }
});

app.listen(port_app, hostname, () => {
    console.log(`Server running at:`);
    console.log('http://' + hostname + ':' + port_app);
});