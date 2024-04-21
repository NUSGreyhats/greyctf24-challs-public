#include <stdio.h>
#include <stdlib.h>

typedef struct slingring {
  char dest[0x80];
  int amt;
} slingring_t;

static slingring_t* rings[10];

void setup() {
  setbuf(stdin, 0);
  setbuf(stdout, 0);
}

void cls() {
  printf("\033[0;33m");
}

void announcement() {
  printf("\033[0;35m");
}

void errorcl() {
  printf("\033[0;31m");
}

void show_slingrings() {
  announcement();
  printf("[Slot]        | [Amt] | [Destination]\n");
  for (int i = 0; i < 10; i++) {
    if (rings[i]) {
      printf("Ring Slot #%d  | [%d]   | %s\n", i, rings[i]->amt, rings[i]->dest);
    } else {
      printf("Ring Slot #%d  | EMPTY\n", i);
    }
  }
  cls();
  printf("Press ENTER to return.\n");
  getchar();
}

void forge_slingring() {
  char input[0x80];
  char destInput[0x80];
  int amtInput;
  int destId;
  printf("Welcome to the ring forge!\n");
  printf("Which slot do you want to store it in? (0-9)\nThis will override any existing rings!\n");
  fgets(input, 4, stdin);
  destId = atoi(input);
  fflush(stdin);
  if (destId > 9 || destId < 0) {
    errorcl();
    printf("Invalid amount!\n");
    printf("Press ENTER to go back...\n");
    getchar();
    return;
  }
  printf("Enter destination location:\n");
  fgets(input, 0x80, stdin);
  *destInput = *input;
  fflush(stdin);
  printf("Enter amount of rings you want to forge (1-9):\n");
  fgets(input, 4, stdin);
  amtInput = atoi(input);
  fflush(stdin);
  if (amtInput > 9 || amtInput < 1) {
    errorcl();
    printf("Invalid amount!\n");
    printf("Press ENTER to go back...\n");
    getchar();
    return;
  }
  rings[destId] = (slingring_t*) malloc(sizeof(slingring_t));
  rings[destId]->amt = amtInput;
  *(rings[destId]->dest) = *destInput;
  announcement();
  printf("New ring forged!\n");
  printf("%d rings going to location [%s] forged and placed in slot %d.\n", rings[destId]->amt, rings[destId]->dest, destId);
  cls();
  printf("Press ENTER to return.\n");
  getchar();
  return;
}

void discard_slingring() {
  char input[4];
  int idx;
  printf("Which ring would you like to discard?\n");
  fgets(input, 4, stdin);
  fflush(stdin);
  idx = atoi(input);
  if (idx < 0 || idx > 9) {
    errorcl();
    printf("Invalid index!\n");
    printf("Press ENTER to go back...\n");
    getchar();
    return;
  }
  announcement();
  if (rings[idx]) {
    free(rings[idx]);
    printf("Ring Slot #%d has been discarded.\n", idx);
    cls();
  } else {
    printf("The ring slot is already empty!\n");
  }
  return;
}

int use_slingring() {
  char spell[0x33];
  char id[4];
  int inputVal;
  printf("Which ring would you like to use (id): ");
  fgets(id, 4, stdin);
  fflush(stdin);
  inputVal = atoi(id);
  printf("\nPlease enter the spell: ");
  fgets(spell, 0x100, stdin);
  printf("\nThank you for visiting our factory! We will now transport you.\n");
  printf("\nTransporting...\n");
}

void menu() {
  char input[4];
  while(1) {
    cls();
    printf("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n");
    printf("Welcome to my secret sling ring factory.\n");
    printf("What do you want to do today?\n\n");
    printf("1. Show Forged Rings\n");
    printf("2. Forge Sling Ring\n");
    printf("3. Discard Sling Ring\n");
    printf("4. Use Sling Ring\n");
    printf(">> ");
    fgets(input, 4, stdin);
    fflush(stdin);
    printf("\n");
    switch(atoi(input)) {
      case 1:
        show_slingrings();
        break;
      case 2:
        forge_slingring();
        break;
      case 3:
        discard_slingring();
        break;
      case 4:
        use_slingring();
        exit(0);
      default:
        printf("Invalid input!\n");
        printf("Press ENTER to go back...\n");
        getchar();
        break;
  }
  }
}

int main() {
  setup();
  char input[6];
  printf("What is your name?\n");
  fgets(input, 6, stdin);
  printf("Hello, ");
  printf(input);
  printf("\n");
  fflush(stdin);
  menu();
}