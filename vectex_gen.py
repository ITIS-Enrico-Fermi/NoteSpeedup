#!/bin/python3

import argparse
from enum import Enum

class VectorDirection(Enum):
	VERTICAL = "\\\\"
	HORIZONTAL = "&"

def genericSizeVector(elementName: str, size: str, delimiter: str) -> str:
	vectorContent = f"{elementName}_{{1}} {delimiter} {elementName}_{{2}} ... {delimiter} {elementName}_{{{size}}} "

	return vectorContent

def concreteSizeVector(elementName: str, size: int, delimiter: str) -> str:
	vectorContent = ""

	for i in range(1, size+1):
		vectorContent += f"{elementName}_{{{i}}}"
		if i != size:
			vectorContent += f" {delimiter} "
	
	return vectorContent

def main(elementName: str, size: str, direction: VectorDirection):
	unformattedDelimiters = "\\begin{{pmatrix}} {} \end{{pmatrix}}"
	
	vectorContent = \
		concreteSizeVector(elementName, int(size), direction.value)	 if size.isnumeric() \
		else genericSizeVector(elementName, size, direction.value)
	
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
	selectDirection = parser.add_mutually_exclusive_group(required=True)
	selectDirection.add_argument("--vertical", help="Generate a vertical vector", action="store_true")
	selectDirection.add_argument("--horizontal", help="Generate an horizontal vector", action="store_true")
	args = parser.parse_args()
	main(args.element, args.size, VectorDirection.VERTICAL if args.vertical else VectorDirection.HORIZONTAL)
