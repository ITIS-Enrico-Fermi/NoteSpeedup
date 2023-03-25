#!/usr/bin/env python3

import argparse

def diagoOnly(elementName: str, maxRowIndex: str, maxColIndex: str) -> str:
	matrixContent = \
		f"{elementName}_{{11}} & \\ & \\ & 0 \\\\ " \
		f"\\ & {elementName}_{{22}} & \\  & \\  \\\\ " \
		f"\\ & \\  & \\ddots  & \\  \\\\ " \
		f"0 & \\  & \\  & {elementName}_{{{maxRowIndex}{maxColIndex}}}  \\\\ " \

	return matrixContent


def genericSizeMatrix(elementName: str, maxRowIndex: str, maxColIndex: str) -> str:
	matrixContent = \
		f"{elementName}_{{11}} & {elementName}_{{12}} & \dots & {elementName}_{{1{maxColIndex}}} \\\\ " \
		f"{elementName}_{{21}} & {elementName}_{{22}} & \dots & {elementName}_{{2{maxColIndex}}} \\\\ " \
		"\\vdots & \\vdots & \\ddots & \\vdots \\\\ " \
		f"{elementName}_{{{maxRowIndex}1}} & {elementName}_{{{maxRowIndex}2}} & \dots & {elementName}_{{{maxRowIndex}{maxColIndex}}} \\\\"

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

def main(genericMatrix: bool, elementName: str, rowsNumber: str, colsNumber: str, diagonalMatrix: bool):
	unformattedDelimiters = "\\begin{{pmatrix}} {} \end{{pmatrix}}"

	if genericMatrix:
		matrixContent = genericSizeMatrix(elementName, rowsNumber, colsNumber)
	elif diagonalMatrix:
		matrixContent = diagoOnly(elementName, rowsNumber, colsNumber)
	else:
		matrixContent = concreteSizeMatrix(elementName, int(rowsNumber), int(colsNumber))	

	print(
		unformattedDelimiters.format(
			matrixContent
		)
	)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		description = "Command line tool for LaTeX matrix generation"
	)

	ElementsType = parser.add_mutually_exclusive_group(required=True)
	ElementsType.add_argument("-g", "--generic", help="Generate a matrix full of coefficients (without explicit values)", default=False, action="store_true")
	ElementsType.add_argument("-n", "--numerical", help="Generate a numerical matrix (full of scalar values)", default=False, action="store_true")
	
	Compression = parser.add_mutually_exclusive_group(required=True)
	Compression.add_argument("-p", "--compact", help="Generate a compact matrix by omitting central rows and columns", default=False, action="store_true")
	Compression.add_argument("-e", "--expanded", help="Generate a full-size matrix", default=False, action="store_true")
	
	parser.add_argument("-s", "--symbol", help="Specify a generic element name or symbol, usually a letter", type=str, default="c", required=False)

	parser.add_argument("-r", "--rows", help="Matrix rows number. Can be a letter.", type=str, default=None, required=True)
	parser.add_argument("-c", "--columns", help="Matrix columns number. Can be a letter.", type=str, default=None, required=True)
	
	matrixShapeSubparser = parser.add_subparsers(help="Define matrix shape", required=True)
	matrixShapeFull = matrixShapeSubparser.add_parser("full", help="Generate full (complete) matrix")
	matrixShapeEye = matrixShapeSubparser.add_parser("eye", help="Generate identity matrix")
	matrixShapeDiag = matrixShapeSubparser.add_parser("diag", help="Generate diagonal matrix")
	matrixShapeTriu = matrixShapeSubparser.add_parser("triu", help="Generate upper triangular matrix")
	matrixShapeTril = matrixShapeSubparser.add_parser("tril", help="Generate lower triangular matrix")	

	args = parser.parse_args()
	# main(args.generic, args.element, args.rows, args.columns, args.diagonal)
