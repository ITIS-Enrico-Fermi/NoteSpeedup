#!/usr/bin/env python3

import argparse
from math import floor
from enum import Enum

COL_SEP = "&"
ROW_SEP = "\\\\"

class MatrixShape(Enum):
	full, eye, diag, triu, tril = range(5)

	def fullMatrixElement(self, i: int, j: int, e: str, generic: bool) -> str:
		return f"{e}_{{{i}{j}}}"
	
	def eyeMatrixElement(self, i: int, j: int, e: str) -> str:
		return "1" if (i == j) else "0"
	
	def diagMatrixElement(self, i: int, j: int, e: str, generic: bool) -> str:
		return f"{e}_{{{i}{j}}}" if (i == j) else "0"

	def triuMatrixElement(self, i: int, j: int, e: str, generic: bool) -> str:
		return f"{e}_{{{i}{j}}}" if (i >= j) else "0"
	
	def trilMatrixElement(self, i: int, j: int, e: str, generic: bool) -> str:
		return f"{e}_{{{i}{j}}}" if (i <= j) else "0"

	def getElements(self, rows: int, cols: int, element: str, generic: bool) -> (int, int, str):
		for i in range(1, rows+1):
			for j in range(1, cols+1):
				if (self == MatrixShape.full):
					yield i, j, self.fullMatrixElement(i, j, element, generic)
				elif (self == MatrixShape.eye):
					yield i, j, self.eyeMatrixElement(i, j, element)
				elif (self == MatrixShape.diag):
					yield i, j, self.diagMatrixElement(i, j, element, generic)
				elif (self == MatrixShape.triu):
					yield i, j, self.triuMatrixElement(i, j, element, generic)
				elif (self == MatrixShape.tril):
					yield i, j, self.trilMatrixElement(i, j, element, generic)

				yield i, j, f" {COL_SEP} " if (j != cols) else " "

			yield i, j, f"{ROW_SEP} " if (i != rows) else ""

def main(rowsNumber: str, colsNumber: str, elementName: str, generic: bool, compact: bool, shape: MatrixShape):
	buf = "\\begin{pmatrix} "

	for i, j, e in shape.getElements(int(rowsNumber), int(colsNumber), elementName, generic):
		if compact and 3 <= i <= int(rowsNumber) - 1:
			if i != 3 or any(s in e for s in [ROW_SEP, COL_SEP, " "]): continue

			if j in [1, 2, int(colsNumber)]: buf += "\\vdots & "
			elif j == 3: buf += "\\ddots & "
			
			if j == int(colsNumber): buf += ROW_SEP
			
		elif compact and 3 <= j <= int(colsNumber) - 1:  # If the current element is in column that has to be shrinked
			"""
			Omit the element except if it's 3rd column element (but not
			a separator), in that case replace it with 3 horizontal dots
			"""
			buf += "\\dots & " if (j == 3 and COL_SEP not in e) else ""

		else:
			buf += e

	buf += "\\end{pmatrix}"

	print(buf)

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
	
	matrixShapeSubparser = parser.add_subparsers(title="shapes", dest="shape", help="Define matrix shape", required=True)
	matrixShapeFull = matrixShapeSubparser.add_parser("full", help="Generate full (complete) matrix")
	matrixShapeEye = matrixShapeSubparser.add_parser("eye", help="Generate identity matrix")
	matrixShapeDiag = matrixShapeSubparser.add_parser("diag", help="Generate diagonal matrix")
	matrixShapeTriu = matrixShapeSubparser.add_parser("triu", help="Generate upper triangular matrix")
	matrixShapeTril = matrixShapeSubparser.add_parser("tril", help="Generate lower triangular matrix")	

	args = parser.parse_args()
	main(args.rows, args.columns, args.symbol, args.generic, args.compact, MatrixShape[args.shape])
