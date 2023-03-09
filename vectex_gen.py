#!/bin/python3

import argparse

def genericSizeMatrix(elementName: str, maxRowIndex: str, maxColIndex: str) -> str:
	matrixContent = \
		f"a_{{11}} & a_{{12}} ... & a_{{1{maxColIndex}}} \\\\ " \
		f"a_{{21}} & a_{{22}} ... & a_{{2{maxColIndex}}} \\\\ " \
		"\\vdots & \\vdots & \\vdots \\\\ " \
		f"a_{{{maxRowIndex}1}} & a_{{{maxRowIndex}2}} ... & a_{{{maxRowIndex}{maxColIndex}}} \\\\"

	return matrixContent

def concreteSizeMatrix(elementName: str, rowsNumber: int, colsNumber: int) -> str:
	matrixContent = ""

	for r in range(1, rowsNumber+1):
		for c in range(1, colsNumber+1):
			matrixContent += f"a_{{{r}{c}}}"
			if c != colsNumber:
				matrixContent += " & "
			else:
				matrixContent += " \\\\ " if r != rowsNumber else ""
	
	return matrixContent

def main(genericMatrix: bool, elementName: str, rowsNumber: str, colsNumber: str):
	unformattedDelimiters = "\\begin{{pmatrix}} {} \end{{pmatrix}}"
	matrixContent = \
		genericSizeMatrix(elementName, rowsNumber, colsNumber) if genericMatrix \
		else concreteSizeMatrix(elementName, int(rowsNumber), int(colsNumber))	

	print(
		unformattedDelimiters.format(
			matrixContent
		)
	)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-g", "--generic", help="Generate generic size vector", default=False, action="store_true")
	parser.add_argument("-s", "--size", help="Vector size", type=str, default=None, required=True)
	parser.add_argument("-e", "--element", help="Element name", type=str, default="a", required=False)
	args = parser.parse_args()
	main(args.generic, args.element, args.rows, args.columns)
