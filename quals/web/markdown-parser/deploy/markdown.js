function parseMarkdown(markdownText) {
    const lines = markdownText.split('\n');
    let htmlOutput = "";
    let inCodeBlock = false;

    lines.forEach(line => {
        if (inCodeBlock) {
            if (line.startsWith('```')) {
                inCodeBlock = false;
                htmlOutput += '</code></pre>';
            } else {
                htmlOutput += escapeHtml(line) + '\n';
            }
        } else {
            if (line.startsWith('```')) {
                language = line.substring(3).trim();
                inCodeBlock = true;
                // add class to code block for syntax highlighting
                htmlOutput += '<pre><code class="language-' + language + '">';
            } else {
                line = escapeHtml(line);
                line = line.replace(/`(.*?)`/g, '<code>$1</code>');
                // Replace Markdown headings with HTML headings
                line = line.replace(/^(######\s)(.*)/, '<h6>$2</h6>');
                line = line.replace(/^(#####\s)(.*)/, '<h5>$2</h5>');
                line = line.replace(/^(####\s)(.*)/, '<h4>$2</h4>');
                line = line.replace(/^(###\s)(.*)/, '<h3>$2</h3>');
                line = line.replace(/^(##\s)(.*)/, '<h2>$2</h2>');
                line = line.replace(/^(#\s)(.*)/, '<h1>$2</h1>');

                // Replace Markdown bold and italics with HTML bold and italics
                line = line.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
                line = line.replace(/__(.*?)__/g, '<strong>$1</strong>');
                line = line.replace(/\*(.*?)\*/g, '<em>$1</em>');
                line = line.replace(/_(.*?)_/g, '<em>$1</em>');
                htmlOutput += line;
            }
        }
    });

    return htmlOutput;
}

function escapeHtml(text) {
    return text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}


// Example usage
const markdown = `
# Heading 1
This is **bold** and this is _italic_.

## Heading 2
This is a code block:
\`\`\`
console.log("Hello, world!");
\`\`\`
`;

module.exports = {
    parseMarkdown
};
