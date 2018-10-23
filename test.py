#!/usr/bin/python3
import argparse
import multiprocessing
import subprocess

def generateCmd(program, args, core, thread):
	if core == multiprocessing.cpu_count():
		cmd = f'time {program} {thread}'
	else:
		cmd = f'time taskset -c 1-{core} {program} {thread}'
	if args is not None:
		cmd += f' {" ".join(args)}'
	return cmd

def runCmd(cmd, input = None):
	cmd = '/bin/bash -c "' + cmd + '"' # Use bash to run the cmd
	ret = subprocess.run(cmd, input = input, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = True)
	if ret.returncode != 0:
		return None
	return ret.stdout.decode()

def toSecond(executeTime):
	minutes = int(executeTime.split('m')[0])
	seconds = float(executeTime.split('m')[1].split('s')[0])
	return minutes * 60 + seconds

def printTable(data, rowHeaders, columnHeaders):
	s = f' |{"|".join(columnHeaders)}\n'
	for row in range(len(data)):
		s += f'{rowHeaders[row]}'
		for column in range(len(data[0])):
			s += f'|{data[row][column] if data[row][column] is not None else ""}'
		s += '\n'
	cmd = f"column -s '|' -t"
	print(runCmd(cmd, input = s.encode()))

def beginTest(program, args, cores, threads, speedup = False, efficiency = False):
	result = [[None] * len(threads) for _ in range(len(cores))]
	row = 0
	for core in cores:
		column = 0
		singleThreadExecuteTime = 0
		for thread in threads:
			# Run the program base on the argumnets
			cmd = generateCmd(program, args, core, thread)
			output = runCmd(cmd)
			if output is None:
				print('Cannot run the program, do you forgot to provide enough arguments')
				return 1
			# Extract output
			output = output.split()
			estimatedPi = output[0]
			executeTime = toSecond(output[2])
			singleThreadExecuteTime = executeTime if thread == 1 else singleThreadExecuteTime
			# Accept result if the esimated pi is 3.14XXX
			if estimatedPi.startswith('3.14'):
				s = str(executeTime)
				if speedup == True:
					s += f', s={singleThreadExecuteTime / executeTime:.2f}'
				if efficiency == True:
					s += f', e={singleThreadExecuteTime / executeTime / thread:.2f}'
				result[row][column] = s
			column += 1
		row += 1
	printTable(result, [f'{core}-core' for core in cores], [f'{thread}-thread' for thread in threads])
	return 0

def main():
	# Parse argument
	parser = argparse.ArgumentParser(description = "A program to test multi-threaded program's performance")
	parser.add_argument('program', type = str, nargs = '?', default = './pi', help = 'Program to be tested')
	parser.add_argument('-a', '--args', dest = 'programArgs', type = str, nargs = '+',help = 'Arguments to be passed to that program')
	parser.add_argument('-s', '--speedup', dest = 'speedup', action='store_true',help = 'Show speedup or not')
	parser.add_argument('-e', '--efficiency', dest = 'efficiency', action='store_true',help = 'Show efficiency or not')
	args = parser.parse_args()
	# Set core and thread to run the program
	core = multiprocessing.cpu_count()
	cores = []
	while core > 0:
		cores += [core]
		core = core >> 1
	threads = [1, 2, 4, 8, 16]
	# Begin to test the performance of the program
	beginTest(args.program, args.programArgs, cores, threads, args.speedup, args.efficiency)

if __name__ == '__main__':
	main()
