import heapq
import fnmatch
import os
import sys

# Name: hw.py
# Author: Zilong Wang
# Goal: merge any number of sorted text files with one data per line into a single file.
# Requirements:
# 	1. The program must compile and run without errors on the sample input files.
# 	2. The program should be self-documenting. Running the program with no input arguments
#   	  should produce instructions. The program should require no input from the user except
#     	arguments passed on the command line when executing the program. Do not prompt the user
#     	for input.
# 	3. The program should be able to handle input files too large to fit entirely in memory.
# 	4. The program should be able to handle merging a file with itself any number of times.
# 	5. The program must be robust. It should not crash or show low-level generic exceptions or
#      stack traces if given unexpected or invalid input.
def main():
	try:
		file_names=[]
		args=sys.argv

		#If no input argument for file names are found, the default is to
		#check for all the .txt files in the current directory and use them as input files.
		if len(args) == 1:	
			for file in os.listdir('.'):
				if fnmatch.fnmatch(file, '*.txt'):
					file_names.append(file)
		#If input file names are provided as command line arguments,
		#use them as input files.
		elif len(args)>1:
			file_names=args[1:]
		merge(file_names)

	except:
	    print "Unexpected error in main():", sys.exc_info()[0]


def merge(file_names):
	try:
		#create a priority queue for maintaining the current smallest strings from each file.
		pq=[]
		opened_files = [ open(f) for f in file_names]
		output_file_name = "output.txt"
		if os.path.isfile(output_file_name):
			f= open(output_file_name,'w+')
			f.close()
		# 	print "file exists"
		# 	os.remove(output_file_name)

		for cur_file in opened_files:
			first = cur_file.readline().rstrip()
			#detect empty file
			if (len(first) is 0):
				continue
			heapq.heappush(pq,(first,cur_file))

		output = open(output_file_name,'w+')

		#keep popping from the priority queue until it is empty.
		while(pq):
			cur = heapq.heappop(pq)
			output.write(cur[0]+'\n')
			print cur[0]
			next=cur[1].readline()
			if len(next) >0:
				next=next.rstrip()
				# check if the input file is sorted properly.
				# if the file is not sorted, raise exception.
				if next<cur[0]:
					raise ValueError('The input file is not sorted properly for ' + cur[1].name +".Please fix it and try again.")
				#put the next smallest item in the queue
				heapq.heappush(pq,(next,cur[1]))

		for f in opened_files:
			f.close() 
		output.close()

	except ValueError as err:
	    print(err.args)
	except:
	    print "Unexpected error in merge():", sys.exc_info()[0]

if __name__ == "__main__":
	main()