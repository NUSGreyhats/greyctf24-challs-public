const express = require('express');
const app = express();
const port = 3000;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.get('/', (req, res) => {
    res.send(`
        <h2>Submit a Pug Template</h2>
        <form action="/render" method="post">
            <textarea name="template" rows="10" cols="50" placeholder="Enter Pug template here..."></textarea>
            <br>
            <input type="submit" value="Render Template">
        </form>
    `);
});

app.post('/render', (req, res) => {
    const {template} = req.body;

    try {
        var lex = require('pug-lexer');
        var parse = require('pug-parser');
        var wrap = require('pug-runtime/wrap');
        var generateCode = require('pug-code-gen');

        const ast = parse(lex(template));
        const whitelistedNodes = ['Tag', 'Text', 'Comment', 'Block', 'Doctype', 'NamedBlock'];
        const filterNodes = (node) => {
            if (whitelistedNodes.includes(node.type)) {
                if (node.nodes) {
                    node.nodes = node.nodes.map(filterNodes).filter(Boolean);
                }
                if (node.block) {
                    node.block = filterNodes(node.block);
                }
                return node;
            }
        };
        const filteredAst = filterNodes(ast); 
        const validateAttrs = (node) => {
            if (node.attrs) {
                node.attrs.forEach(attr => {
                    if (!/^(['"])(?:(?:(?!\1).)|\\.)*\1$/.test(attr.val)) {
                        throw new Error('Invalid attribute value: ' + attr.val);
                    }
                });
            }
            if (node.nodes) {
                node.nodes.forEach(validateAttrs);
            }
            if (node.block) {
                validateAttrs(node.block);
            }
        }; 
        validateAttrs(filteredAst);
        const code = generateCode(filteredAst);
        const html = wrap(code)();

        res.send(html);
    } catch (error) {
        res.status(400).send(`Error rendering template: ${error.message}`);
    }
});

app.listen(port, () => {
    console.log(`Pug to HTML service running at http://localhost:${port}`);
});
