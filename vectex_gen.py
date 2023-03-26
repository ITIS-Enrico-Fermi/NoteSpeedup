#!/usr/bin/env python3

import argparse
from enum import Enum

class VectorDirection(Enum):
	column = "\\\\"
	row = "&"

def genericSizeVector(elementName: str, size: str, delimiter: str) -> str:
	vectorContent = f"{elementName}_{{1}} {delimiter} {elementName}_{{2}} {delimiter} ... {delimiter} {elementName}_{{{size}}} "

	return vectorContent

def concreteSizeVector(elementName: str, size: int, delimiter: str) -> str:
	vectorContent = ""

	for i in range(1, size+1):
		vectorContent += f"{elementName}_{{{i}}}"
		if i != size:
			vectorContent += f" {delimiter} "
	
	return vectorContent

def canonicalVector(elementName: str, size: int, delimiter: str, canonicalPos: int) -> str:
	vectorContent = ""

	for i in range(1, size+1):
		vectorContent += "0" if i != canonicalPos else "1"

		if i != size:
			vectorContent += f" {delimiter} "
	
	return vectorContent

def main(elementName: str, size: str, canonicalPos: int, direction: VectorDirection):
	unformattedDelimiters = "\\begin{{pmatrix}} {} \end{{pmatrix}}"
	
	if size.isnumeric() and not canonicalPos:
		vectorContent = concreteSizeVector(elementName, int(size), direction.value)
	elif size.isnumeric() and canonicalPos:
		vectorContent = canonicalVector(elementName, int(size), direction.value, canonicalPos)
	elif not size.isnumeric() and not canonicalPos:
		vectorContent = genericSizeVector(elementName, size, direction.value)
	else:
		raise ValueError("Invalid options configuration")

	print(
		unformattedDelimiters.format(
			vectorContent
		)
	)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		description = "Command line tool for LaTeX vector generation"
	)

	parser.add_argument("-l", "--length", help="Vector length. Can be either an integer or an index (last index of a generic size vector)", type=str, default=None, required=True)
	parser.add_argument("-s", "--symbol", help="Specify a generic element name or symbol, usually a letter", type=str, default="c", required=False)
	parser.add_argument("-e", "--canonical-vector", help="Generate canonical vector with 1 in the specified position. Eg: e2 = (0 1 0 ... 0)", type=int, required=False)

	selectDirection = parser.add_subparsers(title="directions", dest="direction", help="Define vector direction", required=True)
	selectDirection.add_parser("column", help="Generate a vertical vector")
	selectDirection.add_parser("row", help="Generate an horizontal vector")

	args = parser.parse_args()
	main(args.symbol, args.length, args.canonical_vector, VectorDirection[args.direction])
