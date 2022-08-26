const helper = {
    /** This function generates the error time in datetime format */  
    getErrorTime : function () {
        var currentdate = new Date();
        return currentdate;
    },

    displayError : function (errorMsg) {
        let errorDateTime = getErrorTime();
        console.log("======================");
        console.log(errorMsg);
        console.log("@ " + errorDateTime);
        console.log("======================");
    },
    /** This function checks if the dev type in the topic is either master or edge */
    checkDevType : function (devTopic) {
        if (devTopic.includes("master") || devTopic.includes("edge")) return true;
        else return false;
    },

    /** This function assumes that location is either master or edge */
    hasNan : function (location, data) {
        var boolVal;
        if(location.includes("master")) {
        //If either are NaN
        if(isNaN(data.node_id) || isNaN(data.datetime) || isNaN(data.temperature) || isNaN(data.pressure) || isNaN(data.humidity)) {
            console.log("NaN Detected");
            boolVal = true;
        } else {
            console.log("None are NaN");
            boolVal = false; //none are nan
        }
        } else { //If edge
        if(isNaN(data.node_id) || isNaN(data.datetime) || isNaN(data.light_intensity)) {
            boolVal = true;
        } else {
            console.log("None are NaN");
            boolVal = false; //none are nan
        }
        }
    
        return boolVal;
    },

    /** This function parses the data based on the location to fit a certain table */
    parseData : function (raw_data, location) {
        if(location.includes("master")) {
            try {
                let numId = raw_data["hostname"]["0"].charAt(1);
                console.log("Num id: " + numId);
                let node_id = parseInt(numId);
                let datetime = new Date(raw_data["datetime"]["0"]);
                let temperature = parseFloat(raw_data["temperature"]["0"]);
                let pressure = parseFloat(raw_data["pressure"]["0"]);
                let humidity = parseFloat(raw_data["humidity"]["0"]);
                let data = {node_id: node_id, datetime: datetime, temperature: temperature, pressure: pressure, humidity: humidity};
                return data;
            } catch (e) {
                console.log("Something happpened in the parsing of data. Returning Null...");
                return null;
            }
        } 
        else if (location.includes("edge")) {
            try{
                let numId = raw_data["hostname"]["0"].charAt(1);
                console.log("Num id: " + numId);
                let node_id = parseInt(numId);
                let datetime = new Date(raw_data["datetime"]["0"]);
                let light_intensity = parseFloat(raw_data["lightintensity"]["0"]);
                let data = {node_id: node_id, datetime: datetime, light_intensity: light_intensity}
                return data; 
            } catch (e) {
                console.log("Something happpened in the parsing of data. Returning Null...");
                return null;
            }
        }
    }
}

/* Exports the object `database` (defined above) when another script exports from this file */
module.exports = helper;


