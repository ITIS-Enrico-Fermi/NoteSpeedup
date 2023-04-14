#!/usr/bin/env python3

import argparse
from math import ceil
from enum import Enum
from typing import *

COL_SEP = " & "
ROW_SEP = "\\\\"

COMPACT_ROWS_NUMBER = 4		# < number of rows when using compact rows -cr
COMPACT_COLUMNS_NUMBER = 4	# < number of columns when using compact column -cc

class MatrixShape(Enum):
	full, eye, diag, triu, tril, custom = range(6)

class Matrix():

	def __init__(self, rows: int, cols: int, lastRow: str, lastCol: str, element: str, generic: bool, shape: MatrixShape):
		self.rowsNumber = rows
		self.colsNumber = cols
		self.lastRow = lastRow	# < symbol of the last row if row dimension is generic (for example m), empty string otherwise
		self.lastCol = lastCol	# < symbol of the last column if column dimension is generic (for example n), empty string otherwise
		self.element = element
		self.generic = generic
		self.shape = shape

	def setCustomElementsList(self, elementsList: List[str]) -> None:
		self.customElementsList = elementsList

	def fullMatrixElement(self, i: int, j: int) -> str:
		rowIdx: str = self.lastRow if (self.lastRow and i == self.rowsNumber) else str(i)
		colIdx: str = self.lastCol if (self.lastCol and j == self.colsNumber) else str(j)

		return f"{self.element}_{{{rowIdx}{colIdx}}}" if self.generic else str(i*j)
	
	def eyeMatrixElement(self, i: int, j: int) -> str:
		return "1" if i == j else "0"
	
	def diagMatrixElement(self, i: int, j: int) -> str:
		if i != j: return "0"

		rowIdx: str = self.lastRow if (self.lastRow and i == self.rowsNumber) else str(i)
		colIdx: str = self.lastCol if (self.lastCol and j == self.colsNumber) else str(j)

		return f"{self.element}_{{{rowIdx}{colIdx}}}" if self.generic else str(i*j)

	def triuMatrixElement(self, i: int, j: int) -> str:
		if i > j: return "0"

		rowIdx: str = self.lastRow if (self.lastRow and i == self.rowsNumber) else str(i)
		colIdx: str = self.lastCol if (self.lastCol and j == self.colsNumber) else str(j)

		return f"{self.element}_{{{rowIdx}{colIdx}}}" if self.generic else str(i*j)
	
	def trilMatrixElement(self, i: int, j: int) -> str:
		if i < j: return "0"

		rowIdx: str = self.lastRow if (self.lastRow and i == self.rowsNumber) else str(i)
		colIdx: str = self.lastCol if (self.lastCol and j == self.colsNumber) else str(j)

		return f"{self.element}_{{{rowIdx}{colIdx}}}" if self.generic else str(i*j)

	def customMatrixElement(self, i: int, j: int) -> str:
		return self.customElementsList[(i-1) * self.colsNumber + (j-1)]

	def elementAt(self, row: int, col: int) -> str:
		if self.shape == MatrixShape.full:
			return self.fullMatrixElement(row, col)
		elif self.shape == MatrixShape.eye:
			return self.eyeMatrixElement(row, col)
		elif self.shape == MatrixShape.diag:
			return self.diagMatrixElement(row, col)
		elif self.shape == MatrixShape.triu:
			return self.triuMatrixElement(row, col)
		elif self.shape == MatrixShape.tril:
			return self.trilMatrixElement(row, col)
		elif self.shape == MatrixShape.custom:
			return self.customMatrixElement(row, col)
		
	def rows(self, compactRows: bool, compactCols: bool):
		"""
		Generates the rows and provides an iterator.
		"""

		for i in range(1, self.rowsNumber + 1):
			row = list()
			collapsedRow = False

			if compactRows and i == COMPACT_COLUMNS_NUMBER - 1:
				collapsedRow = True

			if not compactRows or compactRows and not COMPACT_COLUMNS_NUMBER <= i < self.rowsNumber:
				for j in range(1, self.colsNumber + 1):
					if compactCols and COMPACT_COLUMNS_NUMBER - 1 <= j < self.colsNumber:
						if j == COMPACT_COLUMNS_NUMBER - 1:
							row.append("\\dots" if not collapsedRow else "\\ddots")

					else:
						row.append(self.elementAt(i, j) if not collapsedRow else "\\vdots")

			yield row
			

def main(rowsNumber: str, colsNumber: str, elementName: str, generic: bool, compactRows: bool, compactCols: bool, shape: MatrixShape):
	lastRowSymbol = ""
	lastColSymbol = ""

	if colsNumber.isnumeric():
		colsNumber = int(colsNumber)
	else:
		lastColSymbol = colsNumber
		colsNumber = COMPACT_COLUMNS_NUMBER
		compactCols = True

	if rowsNumber.isnumeric():
		rowsNumber = int(rowsNumber)
	else:
		lastRowSymbol = rowsNumber
		rowsNumber = COMPACT_ROWS_NUMBER
		compactRows = True
	
	if shape == MatrixShape.custom:
		if not compactRows and not compactCols:
			import tui
			shape.setCustomElementsList(tui.startInteractiveScreen(rowsNumber, colsNumber))
		else:
			raise ValueError("Unknown matrix dimensions")

	matrix = Matrix(rowsNumber, colsNumber, lastRowSymbol, lastColSymbol, elementName, generic, shape)
	
	buf = "\\begin{pmatrix} "

	for row in matrix.rows(compactRows, compactCols):
		buf += COL_SEP.join(row) + ROW_SEP
	
	buf += " \\end{pmatrix}"

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
