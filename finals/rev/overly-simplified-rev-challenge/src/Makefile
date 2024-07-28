build:
	gcc -S -masm=intel -Wno-attributes -nostdlib -no-pie -fno-builtin chall.c -o chall.s
	# gcc -g -masm=intel -Wno-attributes -nostdlib -no-pie -fno-builtin chall.c -o chall
	python3 obfuscator.py
	gcc -c chall.s -o tmp.o
	ld tmp.o -o chall
	strip chall
	rm tmp.o
	objcopy --remove-section .comment chall
	objcopy --remove-section .note.gnu.property chall
