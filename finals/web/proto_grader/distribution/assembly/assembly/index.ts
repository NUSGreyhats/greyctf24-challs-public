// Modified from https://github.com/kyranet/levenshtein-wasm/blob/main/assembly/index.ts


// @ts-ignore
@inline function min(d0: i32, d1: i32, d2: i32, bx: i32, ay: i32): i32 {
	return d0 < d1 || d2 < d1
		? d0 > d2
			? d2 + 1
			: d0 + 1
		: bx === ay
			? d1
			: d1 + 1;
}


// Memory offsets of strings
const a = 0;
const b = 100;

// @ts-ignore
@inline
function charCodeAt(base: u32, offset: u32): u8 {
  return load<u8>(base + offset);
}

// @ts-ignore
@inline
function read_arr(offset: u32): u32 {
  return load<u32>(b + 100 + offset * 4);
}

// @ts-ignore
@inline
function set_arr(offset: u32, val: u32): void {
  return store<u32>(b + 100 + offset * 4, val);
}

export function levenshtein(la: u32, lb: u32): u32 {
	// Perform suffix suffix trimming
	while (la > 0 && (charCodeAt(a, la - 1) === charCodeAt(b, lb - 1))) {
		--la;
		--lb;
	}

	// Perform prefix trimming
	let offset: u32 = 0;
	while (offset < la && (charCodeAt(a, offset) === charCodeAt(b, offset))) {
		++offset;
	}

	la -= offset;
	lb -= offset;
	if (la === 0 || lb < 3) {
		return lb;
	}

	let x: u32 = 0;
	let y: u32 = 0;
	let d0: i32;
	let d1: i32;
	let d2: i32;
	let d3: i32;
	let dd: u32 = u32.MAX_VALUE;
	let dy: i32;
	let ay: i32;
	let bx0: i32;
	let bx1: i32;
	let bx2: i32;
	let bx3: i32;

	for (let i: u32 = 0; i < la * 2; ++y) {
		set_arr(i++, y + 1);
		set_arr(i++, charCodeAt(a, offset + y));
	}

	let len: u32 = la * 2 - 1;
	while (x < lb - 3) {
		bx0 = charCodeAt(b, offset + (d0 = x));
		bx1 = charCodeAt(b, offset + (d1 = x + 1));
		bx2 = charCodeAt(b, offset + (d2 = x + 2));
		bx3 = charCodeAt(b, offset + (d3 = x + 3));
		x += 4;
		dd = x;
		for (y = 0; y < len; y += 2) {
			dy = read_arr(y);
			ay = read_arr(y + 1);
			d0 = min(dy, d0, d1, bx0, ay);
			d1 = min(d0, d1, d2, bx1, ay);
			d2 = min(d1, d2, d3, bx2, ay);
			dd = min(d2, d3, dd, bx3, ay);
			set_arr(y, dd);
			d3 = d2;
			d2 = d1;
			d1 = d0;
			d0 = dy;
		}
	}

	while (x < lb) {
		bx0 = charCodeAt(b, offset + (d0 = x));
		dd = ++x;
		for (y = 0; y < len; y += 2) {
			dy = read_arr(y);
			dd = min(dy, d0, dd, bx0, read_arr(y + 1));
			set_arr(y, dd);
			d0 = dy;
		}
	}

	return dd;
}