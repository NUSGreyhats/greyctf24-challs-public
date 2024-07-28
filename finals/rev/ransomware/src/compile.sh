gcc encryptor_nolib.c -o encryptor_nolib -masm=intel -s -nostdlib -nostartfiles
gcc stage1.c -o stage1 -masm=intel -nostdlib -nostartfiles