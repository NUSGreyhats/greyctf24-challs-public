const fs = require("fs");
const code = fs.readFileSync(__dirname + "/grader/grader.wasm");


const util = require("./util.js")
const grader = require("./grader")
const flag = util.config.flag;


const src = JSON.parse(atob(process.argv[2]));

const dst = {};
util.copy(src, dst);

const input = dst["input"];

if (!input) {
    console.log("???");
} else {
    console.log(grader(code, input, flag));
}
