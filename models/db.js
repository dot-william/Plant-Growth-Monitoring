const mysql = require('mysql');
const helper  = require('../helperFunction.js');

const database = {
    //Connects to the DB
    connect : function () {
        // Create connection https://pimylifeup.com/raspberry-pi-mysql/
        this.db = mysql.createConnection({
            host : 'localhost',
            user: 'blast',
            password: 'shift12345',
            database: 'pgmsdb'
        });

        this.db.connect(function(err){
            if(err){
              helper.displayError("An error has occured when trying to connect to db.");
              throw err;
            }
            console.log("MySQL Connected...");
        });
    },

    /** This function enters data to a table. If table does not exists it creates a new table
     * @param data data that was parsed from the JSON that was sent to the broker
     * @param db_name name of the database where data will be stored
     * @param location name of the table where data will be stored
     * @param error boolean variable to identify if an error has occured to record error to the table error table
     */
    enterData : function (data, db_name, location) {
        let sql = `SELECT count(*) FROM information_schema.tables
            WHERE table_schema = '${db_name}'
            AND table_name = '${location}';`;

        //Query to check if table exists
        this.db.query(sql, (err, result, fields)=> {
            if(err) {
                console.log("An error has occured when checking table " + location);
                throw err;
            }

            var rows = Object.values(JSON.parse(JSON.stringify(result)))[0];

            // If table does not exist it creates new table based on location
            if(rows['count(*)'] == 0) {
                this.createTable(data, location);
            } else {
                this.insertTable(data, location); //insert to error table
            }
        });
    },
    
    /** This function creates a table 
     * @param data data that was parsed from the JSON that was sent to the broker
     * @param location name of the table where data will be stored
    */
    createTable : function (data, location) { 
        let sql = `CREATE TABLE ${location}(id INT AUTO_INCREMENT, datetime DATETIME, expt_num TINYINT(1), sitename VARCHAR(20), type VARCHAR(25), sensor_idx TINYINT(1), value FLOAT, PRIMARY KEY (id))`;
        this.db.query(sql, (err, result) => {
            if(err) {
                var currentDate = new Date();
                var msg = "[" + currentDate  + "]" + "An error has occured when creating the table @ " + location;
                console.log(msg);
                throw err; 
            }
            //Insert data to table after creating the table
            this.insertTable(data, location);
        });
    },
    
    /** This function inserts data to a specific location
     * @param data data that was parsed from the JSON that was sent to the broker
     * @param location name of the table where data will be stored
     */
    insertTable : function (data, location) {
        console.log(`Table ${location} exists, inserting...`);
        let sql = `INSERT INTO ${location} SET ?`;
        this.db.query(sql, data, (err, result) => {
            if(err) {
                var currentDate = new Date();
                var msg = "[" + currentDate  + "]" + "An error has occured when creating the table @ " + location;
                console.log(msg);
                throw err; 
            }
            helper.logMessage(`Data successfully inserted to ${location} table.`)
            
        });
    },
}

/* Exports the object `database` (defined above) when another script exports from this file */
module.exports = database;

