#include <stdio.h>
#include <stdlib.h>

int main() {
	FILE *inp = fopen("data2.txt", "r+");
	FILE *out = fopen("toPlot2.txt", "w+");
	
	char ch;
	int moves = 0;
	int fruits = 0;
	int episodes = 0;

	while ((ch = fgetc(inp)) != EOF) {
		if (ch == '\n')
			continue;
		if (ch == 'M') {
			moves++;
			//printf("%d\n", moves);
			continue;
		}
		if (ch == 'F') {
			fruits++;
			continue;
		}
		if (ch == 'E') {
			episodes++;
			fprintf(out, "%d\t%d\t%d\n", episodes, moves, fruits);
			moves = 0;
			fruits = 0;
			continue;
		}
	}


	fclose(inp);
	fclose(out);

	return 42;
}