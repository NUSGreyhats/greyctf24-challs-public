const express = require('express');
const bodyParser = require('body-parser');
const util = require('util');
const app = express();
const port = 3000

const mysql = require("mysql");
const config = require("./config.json");

let connection = mysql.createConnection({
    host: config.host,
    user: config.user,
    password: config.password,
    database: config.database,
});

let query = util.promisify(connection.query).bind(connection);

function conn() {
    connection.connect(async function (err) {
        if (err) {
            // Try again, maybe database not started yet
            console.log(err);
            connection = mysql.createConnection({
                host: config.host,
                user: config.user,
                password: config.password,
                database: config.database,
            });
            query = util.promisify(connection.query).bind(connection);
            setTimeout(conn, 10_000);
            return;
        }
        console.log("Connected!");
    
        // Run migrations on startup
        await query("drop table if exists tokens");
        await query("drop table if exists users");
    
        await query("create table tokens(token varchar(255))")
        await query(`create table users(
            id INT AUTO_INCREMENT PRIMARY KEY,
            name varchar(255),
            password varchar(255),
            admin bool
        )`)
    
        console.log("Migration completed!");
    });
}

conn();

app.use(bodyParser.urlencoded({ extended: false }))

app.use("/", express.static("static"))

const decode = s => atob(s?.toString() ?? 'Z3JleWhhdHMh');

app.post('/api/login', async (req, res) => {
    try {
        let { password, username } = req.body;
        password = decode(password);
        username = decode(username);

        const result = await query("select admin from users where name = ? and password = ?", [username, password]);

        if (result.length != 1) {
            return res.json({ err: "Username or password did not match" });
        }

        if(result[0].admin) {
            res.json({ "err": false, "msg": config.flag});
        } else {
            res.json({ "err": false, "msg": "You've logged in successfully, but there's no flag here!"});
        }

        // Prevent too many records from filling up the database
        await query("delete from users where name = ? and password = ?", [username, password]);
    } catch (err) {
        console.log(err);
        res.json({ "err": true });
    }
})

app.post('/api/register/1', async (req, res) => {
    try {
        let { username } = req.body;

        username = decode(username);

        const token = btoa(JSON.stringify({
            name: username,
            admin: false
        }));

        await query("insert into tokens values (?)", [token]);

        res.json({ "err": false, "token": token });
    } catch (err) {
        console.log(err);
        res.json({ "err": true });
    }
})

app.post('/api/register/2', async (req, res) => {
    try {
        let { password, token } = req.body;
        password = decode(password);
        token = decode(token);

        const result = await query("select 1 from tokens where token = ?", [token]);

        if (result.length != 1) {
            return res.json({ err: "Token not found!" });
        }

        await query("delete from tokens where token = ?", [token]);

        const { name, admin } = JSON.parse(atob(token));

        await query("insert into users (name, password, admin) values (?, ?, ?)", [name.toString(), password, admin === true]);

        res.json({ "err": false });
    } catch (err) {
        console.log(err);
        res.json({ "err": true });
    }
})

app.listen(port, () => {
    console.log(`CosmoCraft Collective listening on port ${port}`)
})