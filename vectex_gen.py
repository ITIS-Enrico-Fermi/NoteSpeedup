#!/bin/python3

import argparse

def genericSizeVector(elementName: str, size: str) -> str:
	vectorContent = f"{elementName}_{{1}} & {elementName}_{{2}} ... & {elementName}_{{{size}}} "

	return vectorContent

def concreteSizeVector(elementName: str, size: int) -> str:
	vectorContent = ""

	for i in range(1, size+1):
		vectorContent += f"{elementName}_{{{i}}}"
		if i != size:
			vectorContent += " & "
	
	return vectorContent

def main(elementName: str, size: str):
	unformattedDelimiters = "\\begin{{pmatrix}} {} \end{{pmatrix}}"
	vectorContent = \
		concreteSizeVector(elementName, int(size))	 if size.isnumeric() \
		else genericSizeVector(elementName, size)

	print(
		unformattedDelimiters.format(
			vectorContent
		)
	)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		description = "Command line tool for LaTeX vector generation"
	)
	parser.add_argument("-s", "--size", help="Vector size. Can be either an integer or an index (last index of a generic size vector)", type=str, default=None, required=True)
	parser.add_argument("-e", "--element", help="Element name", type=str, default="a", required=False)
	args = parser.parse_args()
	main(args.element, args.size)
