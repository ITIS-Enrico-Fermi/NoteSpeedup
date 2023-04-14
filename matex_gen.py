#!/usr/bin/env python3

import argparse
from math import ceil
from enum import Enum
from typing import *

COL_SEP = "&"
ROW_SEP = "\\\\"

class MatrixShape(Enum):
	full, eye, diag, triu, tril, custom = range(6)

class Matrix():

	def __init__(self, rows: int, cols: int, lastRow: str, lastCol: str, element: str, generic: bool, shape: MatrixShape):
		self.rows = rows
		self.cols = cols
		self.lastRow = lastRow
		self.lastCol = lastCol
		self.element = element
		self.generic = generic
		self.shape = shape

	def setCustomElementsList(self, elementsList: List[str]) -> None:
		self.customElementsList = elementsList

	def fullMatrixElement(self, i: int, j: int) -> str:
		rowIdx: str = self.lastRow if (self.lastRow and i == self.rows) else str(i)
		colIdx: str = self.lastCol if (self.lastCol and j == self.cols) else str(j)

		return f"{self.element}_{{{rowIdx}{colIdx}}}" if self.generic else str(self.counter)
	
	def eyeMatrixElement(self, i: int, j: int) -> str:
		return "1" if i == j else "0"
	
	def diagMatrixElement(self, i: int, j: int) -> str:
		if i != j: return "0"

		rowIdx: str = self.lastRow if (self.lastRow and i == self.rows) else str(i)
		colIdx: str = self.lastCol if (self.lastCol and j == self.cols) else str(j)

		return f"{self.element}_{{{rowIdx}{colIdx}}}" if self.generic else str(self.counter)

	def triuMatrixElement(self, i: int, j: int) -> str:
		if i > j: return "0"

		rowIdx: str = self.lastRow if (self.lastRow and i == self.rows) else str(i)
		colIdx: str = self.lastCol if (self.lastCol and j == self.cols) else str(j)

		return f"{self.element}_{{{rowIdx}{colIdx}}}" if self.generic else str(self.counter)
	
	def trilMatrixElement(self, i: int, j: int) -> str:
		if i < j: return "0"

		rowIdx: str = self.lastRow if (self.lastRow and i == self.rows) else str(i)
		colIdx: str = self.lastCol if (self.lastCol and j == self.cols) else str(j)

		return f"{self.element}_{{{rowIdx}{colIdx}}}" if self.generic else str(self.counter)

	def customMatrixElement(self, i: int, j: int) -> str:
		return self.customElementsList[(i-1) * self.cols + (j-1)]

	def elements(self) -> (int, int, str):
		for i in range(1, rows+1):
			for j in range(1, cols+1):
				self.counter += 1
				
				if self == MatrixShape.full:
					yield i, j, self.fullMatrixElement(i, j)
				elif self == MatrixShape.eye:
					yield i, j, self.eyeMatrixElement(i, j)
				elif self == MatrixShape.diag:
					yield i, j, self.diagMatrixElement(i, j)
				elif self == MatrixShape.triu:
					yield i, j, self.triuMatrixElement(i, j)
				elif self == MatrixShape.tril:
					yield i, j, self.trilMatrixElement(i, j)
				elif self == MatrixShape.custom:
					yield i, j, self.customMatrixElement(i, j)

				yield i, j, f" {COL_SEP} " if j != cols else " "

			yield i, j, f"{ROW_SEP} " if i != rows else ""

def main(rowsNumber: str, colsNumber: str, elementName: str, generic: bool, compactRows: bool, compactCols: bool, shape: MatrixShape):
	buf = "\\begin{pmatrix} "

	lastRowSymbol = ""
	lastColSymbol = ""

	if colsNumber.isnumeric():
		colsNumber = int(colsNumber)
	else:
		lastColSymbol = colsNumber
		colsNumber = 4
		compactCols = True

	if rowsNumber.isnumeric():
		rowsNumber = int(rowsNumber)
	else:
		lastRowSymbol = rowsNumber
		rowsNumber = 4
		compactRows = True
	
	if shape == MatrixShape.custom:
		if not compactRows and not compactCols:
			import tui
			shape.setCustomElementsList(tui.startInteractiveScreen(rowsNumber, colsNumber))
		else:
			raise ValueError("Unknown matrix dimensions")

	matrix = Matrix(rowsNumber, colsNumber, lastRow, lastCol, element, generic, shape)

	for i, j, e in matrix.elements():
		if compactRows and 3 <= i <= rowsNumber - 1:
			if i != 3 or any(s in e for s in [ROW_SEP, COL_SEP, " "]): continue

			if j == 3 and compactCols: buf += "\\ddots & "
			elif not compactCols or j in [1, 2, colsNumber]: buf += "\\vdots & "
			
			if j == colsNumber: buf += ROW_SEP
			
		elif compactCols and 3 <= j <= colsNumber - 1:
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
	
	parser.add_argument("-cr", "--compact-rows", help="Generate a compact matrix by omitting central rows", default=False, action="store_true")
	parser.add_argument("-cc", "--compact-cols", help="Generate a compact matrix by omitting central columns", default=False, action="store_true")
	
	parser.add_argument("-s", "--symbol", help="Specify a generic element name or symbol, usually a letter", type=str, default="c", required=False)

	parser.add_argument("-r", "--rows", help="Matrix rows number. Can be a letter.", type=str, default=None, required=True)
	parser.add_argument("-c", "--columns", help="Matrix columns number. Can be a letter.", type=str, default=None, required=True)
	
	matrixShapeSubparser = parser.add_subparsers(title="shapes", dest="shape", help="Define matrix shape", required=True)
	matrixShapeSubparser.add_parser("full", help="Generate full (complete) matrix")
	matrixShapeSubparser.add_parser("eye", help="Generate identity matrix")
	matrixShapeSubparser.add_parser("diag", help="Generate diagonal matrix")
	matrixShapeSubparser.add_parser("triu", help="Generate upper triangular matrix")
	matrixShapeSubparser.add_parser("tril", help="Generate lower triangular matrix")	
	matrixShapeSubparser.add_parser("custom", help="Interactive screen to fill in the matrix your own way")	

	args = parser.parse_args()
	main(args.rows, args.columns, args.symbol, args.generic, args.compact_rows, args.compact_cols, MatrixShape[args.shape])
