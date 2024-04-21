const express = require('express');
const { parseMarkdown } = require('./markdown.js');
const { visitUrl } = require('./admin.js');
const app = express();
const port = 3000;

// Middleware to parse JSON and URL-encoded bodies
app.use(express.urlencoded({ extended: true }));

// Set the view engine to ejs
app.set('view engine', 'ejs');

app.get('/', (req, res) => {
    // Render 'index.ejs' with dynamic content
    res.render('input', { content: '' });
});

// Route to handle Markdown parsing as a GET request
app.get('/parse-markdown', (req, res) => {
    const base64Markdown = req.query.markdown;
    if (!base64Markdown) {
        return res.status(400).send('No markdown content provided');
    }

    try {
        // Decode Base64 string to Markdown
        const markdown = atob(base64Markdown);
        console.log(markdown)
        const html = parseMarkdown(markdown);
        console.log(html)
        res.render('view', { content: html });
    } catch (error) {
        console.error(error);
        res.status(500).send('Error parsing markdown');
    }
});

app.get('/feedback', async (req, res) => {
    let url = req.query.url
    console.log('received url: ', url)

    let parsedURL
    try {
        parsedURL = new URL(url)
    }
    catch (e) {
        res.send(escape(e.message))
        return
    }

    if (parsedURL.protocol !== 'http:' && parsedURL.protocol != 'https:') {
        res.send('Please provide a URL with the http or https protocol.')
        return
    }

    if (parsedURL.hostname !== req.hostname) {
        res.send(`Please provide a URL with a hostname of: ${escape(req.hostname)}, your parsed hostname was: escape(${parsedURL.hostname})`)
        return
    }

    if(!url.includes("/parse-markdown?")) {
	res.send("Invalid URL!");
        return;
    }

    url = "http://localhost:3000/parse-markdown?"+url.split("/parse-markdown?")[1]

    try {
        console.log('visiting url: ', url)
        await visitUrl(url, 'localhost:3000')
        res.send('The admin has viewed your feedback!')
    } catch (e) {
        console.log('error visiting: ', url, ', ', e.message)
        res.send('Error, admin unable to view your feedback')
    } finally {
        console.log('done visiting url: ', url)
    }

})

// Start the server
app.listen(port, () => {
    console.log(`Markdown parser app listening at http://localhost:${port}`);
});
