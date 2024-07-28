const memory = new WebAssembly.Memory({ initial: 1 });
const imports = {
  env: {
    memory: memory,
  },
};

const buf = new Uint8Array(memory.buffer);


module.exports = (code, input, flag) => {
  for (let i = 0; i < flag.length; i++) {
    buf[i + 100] = flag.charCodeAt(i);
  }

  let input_len = 0;
  while (input_len < 100 && input[input_len] != 0) {
    buf[input_len] = input[input_len];
    input_len++;
  }

  const module = new WebAssembly.Module(code);
  return new WebAssembly.Instance(module, imports).exports.levenshtein(input_len, flag.length);
}