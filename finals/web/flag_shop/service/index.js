const express = require('express');
const session = require('express-session')
const app = express();
app.use(express.json());
app.use(session({
    secret: process.env.SECRET
}))

const dotenv = require('dotenv');
dotenv.config();

const functions = {
    order: require('./functions/order'),
    menu: require('./functions/menu'),
    shop: require('./functions/shop'),
    user: require('./functions/user'),
};

app.get('/healthcheck', (req, res) => {
    res.status(200).send("ok");
});

app.get('/api/:module/:method', async (req, res) => {
    if (!req.session.order) {
        req.session.order = [];
    }
    const { module, method } = req.params;
    const arg = req.query.arg;
    if (!functions[module] || !functions[module][method] || typeof functions[module][method] !== 'function')
        return res.status(404).send("Method not found");
    let callable = functions[module][method];
    return res.status(200).send(JSON.stringify({ result: callable(req.session, arg) }));
});


// Start the server
const port = 33335;
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});