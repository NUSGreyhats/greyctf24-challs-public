
const config = require("../config.json");

function decode_user_hex_string(str) {
    const length = config.size;

    const buf = new Uint8Array(Buffer.from("a".repeat(length)).buffer);

    for (let i = 0; i < length * 2; i += 2) {
        const byte = parseInt(str.substring(i, i + 2), 16);
        if (Number.isNaN(byte)) {
            buf[i >>> 1] = 0;
        }
        buf[i >>> 1] = byte;
    }
    return buf;
}

function is_object(t) {
    return typeof t == "object" && t !== null && !Array.isArray(t);
}

module.exports.copy = function copy(src, dst) {
    for (const key of Object.keys(src)) {
        const val = src[key];
        if (is_object(val)) {
            copy(src[key], dst[key]);
        } else if (typeof val == "string") {
            dst[key] = decode_user_hex_string(src[key]);
        } else {
            dst[key] = src[key];
        }
    }
}

module.exports.config = config;
