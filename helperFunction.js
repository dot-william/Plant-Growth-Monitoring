const helper = {
    
    
    /** This function checks if parsed data contains nan values */
    hasNan : function (data) {
        var boolVal;
        //If either are NaN
        if(isNaN(data.datetime) || isNaN(data.value)) {
            boolVal = true;
        } else {
            boolVal = false; //none are nan
        }
        return boolVal;
    },

    /** This function parses the data based on the location to fit a certain table 
     * @param raw_data the data to be parse
    */
    parseData : function (raw_data) {
        try {
            let datetime = new Date(raw_data["datetime"]["0"]);
            let expt_num = parseInt(raw_data["expt_num"]["0"]);
            let sitename= raw_data["sitename"]["0"];
            let type = raw_data["type"]["0"];
            //insert statement to convert integer to
            let index = parseInt(raw_data["index"]["0"]);
            let value= parseFloat(raw_data["value"]["0"]);
            let data = {datetime: datetime, 
                        expt_num: expt_num, 
                        sitename: sitename, 
                        type: type, 
                        sensor_idx: index,
                        value: value};
            return data;
        } catch (e) {
            console.log("Something happpened in the parsing of data. Returning Null...");
            return null;
        }
    },

    /** This function checks if the topic is valid
     * @param topic topic sent by the broker
     * @param validTopics array of valid topics to cross reference
     * @param validTopicType array of topic type to cross reference e.g. temperature, humidity, etc
     * @returns boolean if the topic is valid or not
     */
    checkTopic : function (topic, validTopics, validTopicType) {
        // Add validation, invalid topic not shift etc, and log the error to the db
        let splittedTopic = topic.split('/');
        let validTopicsLength = (splittedTopic.length - 1);
        let isValid = true;
        let topicType = splittedTopic[validTopicsLength]; //gets the type from the end of the topic 
        let i = 0;

        //Search if topic is valid and its sequence
        while (i < validTopicsLength && isValid) {
            if(splittedTopic[i] != validTopics[i])
                isValid = false;
            i++;
        }
        
        //If it is still valid, check if topic type is valid
        if(isValid) {
            //Initialize first to false
            isValid = false;
            i = 0;
            //Search through the valid topic types (temperature, humidity, etc)
            while (i < validTopicType.length && !isValid) {
                // If the topic is valid set isValid to true to stop loop and return variable
                if(topicType == validTopicType[i])
                    isValid = true; 
                i++;
            }
        
        }
        return isValid;
    },

    getDatetime : function() {
        var currentdate = new Date();
        return currentdate;
    },

    /** This function logs information to the console
     * @param message the message to be displayed
     */
    logMessage : function (message) {
        let currentDate = new Date();
        var logMsg = "[" + currentDate  + "]" + " " + message;
        console.log(logMsg);
    },

    /**
     * This function logs the error message to the database
     * @param  message string that will be stored 
     * @returns object that will be stored to the DB
     */
    errorLog : function (message) {
        let currentDate = new Date();
        let errorMsg = message;
        let errorLog = {datetime: currentDate, msg: errorMsg};
        return errorLog;
    }
}

/* Exports the object `database` (defined above) when another script exports from this file */
module.exports = helper;


