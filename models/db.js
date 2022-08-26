const mysql = require('mysql');
const helper  = require('../helperFunction.js');

const database = {
    //Connects to the DB
    connect : function () {
        // Create connection https://pimylifeup.com/raspberry-pi-mysql/
        const db = mysql.createConnection({
            host : 'localhost',
            user: 'blast',
            password: 'shift12345',
            database: 'shiftdb'
        });

        db.connect(function(err){
            if(err){
              displayError("An error has occured when trying to connect to db.");
              throw err;
            }
            console.log("MySQL Connected...");
        });
    },

    /** Enter data to a table. If table does not exists it creates a new table
     * @param data data that was parsed from the JSON that was sent to the broker
     * @param db_name name of the database where data will be stored
     * @param location name of the table where data will be stored
     * @param error boolean variable to identify if an error has occured to record error to the table error table
     */
    enterData : function (data, db_name, location, error) {

        if(!error) {
            //Query to check if table exists
            let sql = `SELECT count(*) FROM information_schema.tables
            WHERE table_schema = '${db_name}'
            AND table_name = '${location}';`;

            db.query(sql, (err, result, fields)=> {
                if(err) {
                    console.log("An error has occured when checking table " + location);
                    throw err;
                }

                var rows = Object.values(JSON.parse(JSON.stringify(result)))[0];

                // If table does not exist
                if(rows['count(*)'] == 0) {
                    console.log(`Table ${location} does not exists, creating new table...`);
                    // Always either master or edge since it was checked prior
                    if(location.includes("master")) {
                        this.createTable(location, data);
                    } else if (location.includes("edge")) {
                         //Create table then insert
                        let sql = `CREATE TABLE ${location}(
                            id INT(11) AUTO_INCREMENT, 
                            node_id  TINYINT(1), 
                            datetime DATETIME,
                            light_intensity FLOAT, 
                            PRIMARY KEY (id))`
                            }
                        db.query(sql, (err, result) => {
                            if(err) {
                                displayError("An error has occured when creating table " + location);
                                throw err; 
                            }
                            
                            console.log("Table created, inserting data...");
                            let sql = `INSERT INTO ${location} SET ?`;
                            //Query to insert data
                            db.query(sql, data, (err, result) => {
                                if(err) {
                                    helper.displayError("An error has occured when inserting in the table " + location);
                                    throw err; 
                                }
                                console.log(`Data successfully inserted to ${location} table.`);
                            });
                        });
                } else {
                    insertTable(location);
                }
            });
        }
       
    }
    
    createTable : function () {
        let sql = `CREATE TABLE ${location}(
                            id INT(11) AUTO_INCREMENT, 
                            node_id TINYINT(1), 
                            datetime DATETIME,
                            temperature FLOAT,
                            pressure FLOAT,
                            humidity FLOAT, 
                            PRIMARY KEY (id))`;

        db.query(sql, (err, result) => {
            if(err) {
                displayError("An error has occured when creating table " + location);
                throw err; 
            }
            console.log("Table created, inserting data...");
            let sql = `INSERT INTO ${location} SET ?`;
            //Query to insert data
            db.query(sql, data, (err, result) => {
                if(err) {
                    helper.displayError("An error has occured when inserting elements after creating table "  + location);
                    throw err; 
                }
                console.log(`Data successfully inserted to ${location} table.`);
            });
        });
    },
    
    insertTable : function (location) {
        console.log(`Table ${location} exists, inserting...`);
        let sql = `INSERT INTO ${location} SET ?`;
        db.query(sql, data, (err, result) => {
            if(err) {
                displayError("An error has occured when inserting at table " + location );
                throw err; 
            }
            
            console.log(`Data successfully inserted to ${location} table.`);
        });
    }
    /** Gets data based on parameter (to be implemented in the future) 
     * 
     */

    //findData : function (table, query) {
    //     let sql = `SELECT * FROM information_schema.tables`
    // }

}

/* Exports the object `database` (defined above) when another script exports from this file */
module.exports = database;

