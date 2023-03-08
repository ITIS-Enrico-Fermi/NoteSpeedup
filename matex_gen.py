#!/bin/python3

import argparse

def main(genericMatrix: bool, rowsNumber: int, colsNumber: int):
	unformattedDelimiters = "\\begin{{matrix}} {} \end{{matrix}}"
	matrixContent = ""

	for r in range(1, rowsNumber+1):
		for c in range(1, colsNumber+1):
			matrixContent += f"a_{{{r}{c}}}"
			if c != colsNumber:
				matrixContent += " & "
			else:
				matrixContent += " \\\\ " if r != rowsNumber else ""
			
	print(unformattedDelimiters.format(matrixContent))

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-g", "--generic", help="Generate generic matrix", default=False, action="store_true")
	parser.add_argument("-r", "--rows", help="Matrix rows number", type=int, default=None, required=True)
	parser.add_argument("-c", "--columns", help="Matrix columns number", type=int, default=None, required=True)
	args = parser.parse_args()
	main(args.generic, args.rows, args.columns)
