const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const port = 3000

const config = require("./config.json");

app.use(bodyParser.json())

app.use("/", express.static("static"))

let score = -0.42069;

app.get("/status", async (req, res)=>{
    return res.status(200).json({
        "error": false,
        "data": score
    });
})

app.post('/vote', async (req, res) => {
    const {vote} = req.body;
    if(typeof vote != 'number') {
        return res.status(400).json({
            "error": true,
            "msg":"Vote must be a number"
        });
    }
    if(vote < 1 && vote > -1) {
        score += parseInt(vote);
        if(score > 1) {
            score = -0.42069;
            return res.status(200).json({
                "error": false,
                "msg": config.flag,
            });
        }
        return res.status(200).json({
            "error": false,
            "data": score,
            "msg": "Vote submitted successfully"
        });
    } else {
        return res.status(400).json({
            "error": true,
            "msg":"Invalid vote"
        });
    }
})

app.listen(port, () => {
    console.log(`Survey listening on port ${port}`)
})