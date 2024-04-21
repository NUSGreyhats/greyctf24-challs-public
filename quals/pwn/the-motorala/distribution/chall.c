#include <stdio.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>


char* pin;

// this is the better print, because i'm cool like that ;)
void slow_type(char* msg) {
	int i = 0;
	while (1) {
		if (!msg[i])
			return;
		putchar(msg[i]);
		usleep(5000);
		i += 1;
	}
}

void view_message() {
	int fd = open("./flag.txt", O_RDONLY);
	char* flag = calloc(0x50, sizeof(char));
	read(fd , flag, 0x50);
	close(fd);
	slow_type("\n\e[1;93mAfter several intense attempts, you successfully breach the phone's defenses.\nUnlocking its secrets, you uncover a massive revelation that holds the power to reshape everything.\nThe once-elusive truth is now in your hands, but little do you know, the plot deepens, and the journey through the clandestine hideout takes an unexpected turn, becoming even more complicated.\n\e[0m");
	printf("\n%s\n", flag);
	exit(0);
}

void retrieve_pin(){
	FILE* f = fopen("./pin", "r");
	pin = malloc(0x40);
	memset(pin, 0, 0x40);
	fread(pin, 0x30, 0x1, f);
	fclose(f);
}

void login() {
	char attempt[0x30];
	int count = 5;

	for (int i = 0; i < 5; i++) {
		memset(attempt, 0, 0x30);
		printf("\e[1;91m%d TRIES LEFT.\n\e[0m", 5-i);
		printf("PIN: ");
		scanf("%s", attempt);
		if (!strcmp(attempt, pin)) {
			view_message();
		}
	}
	slow_type("\n\e[1;33mAfter five unsuccessful attempts, the phone begins to emit an alarming heat, escalating to a point of no return. In a sudden burst of intensity, it explodes, sealing your fate.\e[0m\n\n");
}

void banner() {

	slow_type("\e[1;33mAs you breached the final door to TACYERG's hideout, anticipation surged.\nYet, the room defied expectations – disorder reigned, furniture overturned, documents scattered, and the vault empty.\n'Yet another dead end,' you muttered under your breath.\nAs you sighed and prepared to leave, a glint caught your eye: a cellphone tucked away under unkempt sheets in a corner.\nRecognizing it as potentially the last piece of evidence you have yet to find, you picked it up with a growing sense of anticipation.\n\n\e[0m");

    puts("                         .--.");
	puts("                         |  | ");
	puts("                         |  | ");
	puts("                         |  | ");
	puts("                         |  | ");
	puts("        _.-----------._  |  | ");
	puts("     .-'      __       `-.  | ");
	puts("   .'       .'  `.        `.| ");
	puts("  ;         :    :          ; ");
	puts("  |         `.__.'          | ");
	puts("  |   ___                   | ");
	puts("  |  (_M_) M O T O R A L A  | ");
	puts("  | .---------------------. | ");
	puts("  | |                     | | ");
	puts("  | |      \e[0;91mYOU HAVE\e[0m       | | ");
	puts("  | |  \e[0;91m1 UNREAD MESSAGE.\e[0m  | | ");
	puts("  | |                     | | ");
	puts("  | |   \e[0;91mUNLOCK TO VIEW.\e[0m   | | ");
	puts("  | |                     | | ");
	puts("  | `---------------------' | ");
	puts("  |                         | ");
	puts("  |                __       | ");
	puts("  |  ________  .-~~__~~-.   | ");
	puts("  | |___C___/ /  .'  `.  \\  | ");
	puts("  |  ______  ;   : OK :   ; | ");
	puts("  | |__A___| |  _`.__.'_  | | ");
	puts("  |  _______ ; \\< |  | >/ ; | ");
	puts("  | [_=]						\n");

	slow_type("\e[1;94mLocked behind a PIN, you attempt to find a way to break into the cellphone, despite only having 5 tries.\e[0m\n\n");
}


void init() {
	setbuf(stdin, 0);
	setbuf(stdout, 0);
	retrieve_pin();
	printf("\e[2J\e[H");
}

int main() {
	init();
	banner();
	login();
}
