#define _GNU_SOURCE

#include <stdio.h>
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>
#include <sys/mman.h>
#include <stdio.h>
#include <ctype.h>
#define STR_VALUE(val) #val
#define STR(name) STR_VALUE(name)
#define PATH_LEN 256
#define MD5_LEN 32
#include <openssl/md5.h>
#include <time.h>
#include <stdlib.h>
#include <unistd.h>

#define CLRSCR "\e[2J\e[H";
#define GHOST_MONTH_START_TIMESTAMP 1722700800

#define ASCII_ART "\e[0;33m⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣴⣶⡶⠶⠶⠶⠿⠿⠿⠿⠶⠶⣶⣦⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n" \
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⣾⡿⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⣷⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n" \
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⠿⠟⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢿⣦⣄⡀⠀⠀⠀⠀⠀⠀\n" \
"⠀⠀⠀⠀⠀⠀⠀⢀⣤⡾⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⢦⡀⠀⠀⠀⠀\n" \
"⠀⠀⠀⠀⠀⢠⣶⡿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣷⡄⠀⠀⠀\n" \
"⠀⠀⠀⢀⣼⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣆⠀⠀\n" \
"⠀⠀⣠⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣦⠀\n" \
"⠀⢀⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣶⣦⡀⠀⠀⠀⠀⠀⠀⠀⠈⣿⡆\n" \
"⠀⣾⡟⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠸⣷\n" \
"⢰⣿⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⢻  \e[0;34mOh dear,\n\e[0;33m" \
"⢸⡏⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⢸  \e[0;34mthe cold,\n\e[0;33m" \
"⣾⡇⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⢸  \e[0;34mquiet,\n\e[0;33m" \
"⣿⡇⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⢸  \e[0;34mslumber?\n\e[0;33m" \
"⢿⡇⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡈⠙⠛⠛⠁⠀⠀⠀⠀⠀⠀⠀⣾\n" \
"⢸⣇⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⠏⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠒⠶⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿  \e[0;34mWhen can I leave...?\n\e[0;33m" \
"⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⣤⡾⢡⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⠏\n" \
"⠀⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⠏⠀  \e[0;34mI'll be waiting for the day\n\e[0;33m" \
"⠀⠀⠻⣷⡂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⡟⠃⠀⠀⠀  \e[0;34mwhen the gates are opened...\n\e[0;33m" \
"⠀⠀⠀⠻⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⡿⠋⠀⠀⠀⠀⠀\n" \
"⠀⠀⠀⠀⠹⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⡿⠋⠀⠀⠀⠀⠀⠀⠀\n" \
"⠀⠀⠀⠀⠀⠈⠻⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⠿⠏⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀\n" \
"⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠿⢶⣦⣤⣤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡴⢿⣿⣥⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n" \
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢉⣻⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠒⠀⠀⠀⠁⠀⠀⠉⠛⢷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n" \
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣶⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣦⠀⠀⠀⠀⠀⠀⠀⠀\n" \
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠀⠀⠀⠀⠙⣷⡄⠀⠀⠀⠀⠀⠀\n" \
"⠀⠀⠀⠀⠀⠀⠀⢀⣾⠟⠁⠀⠀⠀⢀⣀⣤⡤⠗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡀⠀⠀⠀⠈⢿⣆⠀⠀⠀⠀⠀\n" \
"⠀⠀⠀⠀⠀⠀⠀⠘⣿⣶⣶⠶⠿⠟⢻⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣷⣦⣀⠀⠀⠈⢻⡇⠀⠀⠀⠀\n" \
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡏⠻⠿⢶⣶⡾⠇⠀⠀⠀⠀\n" \
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n" \
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n" \
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n" \
"⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n" \
"⣿⣿⣿⡷⣬⠵⣦⢸⣶ \e[0;32m%s\e[0;33m ⠿⢶⡶⠿⣿⣿⣿\n" \
"⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n\e[0m"

char md5_sum[MD5_LEN+1];

void open_the_gate_of_hell() {
	int fp = open("gate.bin", O_RDONLY);
	char* buf = mmap(0x0, 0x1000, 0x7, MAP_PRIVATE | MAP_32BIT, fp, 0);
	*(int*)(buf+0x500) = *(int*)md5_sum;
	memfrob(buf, 0x1000);
	asm(
		".intel_syntax noprefix;"
		"mov rbx, 0x23;"
		"shl rbx, 32;"
		"add rax, rbx;"
		"push rax;"
		".byte 0xcb;"
		".att_syntax;"
	);
}

int CalcFileMD5(char *file_name)
{
	char* md5sum = md5_sum;
	    #define MD5SUM_CMD_FMT "md5sum %." STR(PATH_LEN) "s 2>/dev/null"
	    char cmd[PATH_LEN + sizeof (MD5SUM_CMD_FMT)];
	    sprintf(cmd, MD5SUM_CMD_FMT, file_name);
	    #undef MD5SUM_CMD_FMT

	    FILE *p = popen(cmd, "r");
	    if (p == NULL) return 0;

	    int i, ch;
	    for (i = 0; i < MD5_LEN && isxdigit(ch = fgetc(p)); i++) {
		        *md5sum++ = ch;
		    }

	    *md5sum = '\0';
	    pclose(p);
	    return i == MD5_LEN;
}

int main(int argc, char** argv) {

	CalcFileMD5(argv[0]);
	printf(ASCII_ART, md5_sum);

	if ((time(NULL) == GHOST_MONTH_START_TIMESTAMP) && (ptrace(PTRACE_TRACEME) != -1)) {
		open_the_gate_of_hell(argv[0]);
	}
}
