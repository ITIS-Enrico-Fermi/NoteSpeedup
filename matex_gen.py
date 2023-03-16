 #!/bin/python3

import argparse

def genericSizeMatrix(elementName: str, maxRowIndex: str, maxColIndex: str) -> str:
	matrixContent = \
		f"{elementName}_{{11}} & {elementName}_{{12}} & ... & {elementName}_{{1{maxColIndex}}} \\\\ " \
		f"{elementName}_{{21}} & {elementName}_{{22}} & ... & {elementName}_{{2{maxColIndex}}} \\\\ " \
		"\\vdots & \\vdots & \\ddots & \\vdots \\\\ " \
		f"{elementName}_{{{maxRowIndex}1}} & {elementName}_{{{maxRowIndex}2}} & ... & {elementName}_{{{maxRowIndex}{maxColIndex}}} \\\\"

	return matrixContent

def concreteSizeMatrix(elementName: str, rowsNumber: int, colsNumber: int) -> str:
	matrixContent = ""

	for r in range(1, rowsNumber+1):
		for c in range(1, colsNumber+1):
			matrixContent += f"{elementName}_{{{r}{c}}}"
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
	parser = argparse.ArgumentParser(
		description = "Command line tool for LaTeX matrix generation"
	)
	parser.add_argument("-g", "--generic", help="Generate generic size matrix", default=False, action="store_true")
	parser.add_argument("-r", "--rows", help="Matrix rows number", type=str, default=None, required=True)
	parser.add_argument("-c", "--columns", help="Matrix columns number", type=str, default=None, required=True)
	parser.add_argument("-e", "--element", help="Element name", type=str, default="a", required=False)
	args = parser.parse_args()
	main(args.generic, args.element, args.rows, args.columns)

