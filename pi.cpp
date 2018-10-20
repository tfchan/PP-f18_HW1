#include <iostream>
#include <cstdlib>
#include <ctime>
using namespace std;

const unsigned int NUMBER_OF_TOSS = 10000000;

double monteCarloEstimation(unsigned int numberOfToss) {
	unsigned int numberInCircle = 0;
	double x, y;
	for (unsigned int toss = 0; toss < numberOfToss; toss++) {
		x = (double)rand() / RAND_MAX;
		y = (double)rand() / RAND_MAX;
		if (x * x + y * y <= 1) {
			numberInCircle++;
		}
	}
	return (double)4 * numberInCircle / numberOfToss;
}

int main(int argc, char *argv[]) {
	srand(time(NULL));
	double pi = monteCarloEstimation(NUMBER_OF_TOSS);
	cout << pi << endl;
	return 0;
}
