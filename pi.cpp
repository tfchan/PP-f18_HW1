#include <iostream>
#include <cstdlib>
#include <ctime>
#include <pthread.h>
using namespace std;

void* performToss(void* arg) {
	unsigned long long *numberInCircle = new unsigned long long(0); // Allocate memory to store result, so as to return by thread status
	unsigned long long numberOfToss = *((unsigned long long*)arg);
	double x, y;
	unsigned int seed = time(NULL); // Set seed for rand_r
	// Begin to toss
	for (unsigned long long toss = 0; toss < numberOfToss; toss++) {
		// Random a double between 0 and 1, use rand_r for multi-thread purpose
		x = (double)rand_r(&seed) / RAND_MAX;
		y = (double)rand_r(&seed) / RAND_MAX;
		// Check if the point locate within the circle
		if (x * x + y * y <= 1) {
			(*numberInCircle)++;
		}
	}
	// Return result as exit status
	return (void*)numberInCircle;
}

double monteCarloEstimation(unsigned int numberOfThread, unsigned long long numberOfToss) {
	pthread_t tid[numberOfThread];
	unsigned long long tossPerThread = numberOfToss / numberOfThread;
	unsigned long long tossAtLastThread = numberOfToss - tossPerThread * (numberOfThread - 1);
	// Create thread
	for (unsigned int i = 0; i < numberOfThread; i++) {
		if (i < numberOfThread - 1)
			pthread_create(&tid[i], NULL, performToss, (void*)&tossPerThread);
		else
			pthread_create(&tid[i], NULL, performToss, (void*)&tossAtLastThread);
	}
	unsigned long long *ret;
	unsigned long long numberInCircle = 0;
	// Join thread and get result from return status
	for (unsigned int i = 0; i < numberOfThread; i++) {
		pthread_join(tid[i], (void**)&ret);
		numberInCircle += *ret;
		delete ret; // Delete memory that is allocated in thread
	}
	// Calculte pi
	return (double)4 * numberInCircle / numberOfToss;
}

int main(int argc, char *argv[]) {
	unsigned int numberOfThread;
	unsigned long long numberOfToss;
	// Extract argument
	if (argc != 3 || atoi(argv[1]) <= 0 || atoll(argv[2]) <= 0) {
		cout << "Usage: " << argv[0] << " [Number of thread] [Number of toss]" << endl;
		return 1;
	} else {
		numberOfThread = atoi(argv[1]);
		numberOfToss = atoll(argv[2]);
	}
	// Do estimation
	double pi = monteCarloEstimation(numberOfThread, numberOfToss);
	cout << pi << endl;
	return 0;
}
