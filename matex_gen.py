#!/usr/bin/env python3

import argparse
from math import ceil
from enum import Enum
from typing import *

COL_SEP = " & "
ROW_SEP = "\\\\"

COMPACT_ROWS_NUMBER = 4		# < number of rows when using compact rows -cr
COMPACT_COLUMNS_NUMBER = 4	# < number of columns when using compact column -cc


class Matrix():

	def __init__(self, rows: int, cols: int, lastRow: str, lastCol: str, element: str, generic: bool, diagShift: int):
		self.rowsNumber = rows
		self.colsNumber = cols
		self.lastRow = lastRow	# < symbolic index of the last row if row dimension is generic (for example m), empty string otherwise
		self.lastCol = lastCol	# < symbolic index of the last column if column dimension is generic (for example n), empty string otherwise
		self.element = element
		self.generic = generic
		self.diagShift = diagShift

	def elementAt(self, i: int, j: int) -> str:
		"""
		This method is called by self.rows to retrieve a matrix element at the given indexes.
		A subclass must override this.
		"""
		return ""
		
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

class FullMatrix(Matrix):
	def elementAt(self, i: int, j: int) -> str:
		rowIdx: str = self.lastRow if (self.lastRow and i == self.rowsNumber) else str(i)
		colIdx: str = self.lastCol if (self.lastCol and j == self.colsNumber) else str(j)

		return f"{self.element}_{{{rowIdx}{colIdx}}}" if self.generic else str(i*j)
	
class EyeMatrix(Matrix):
	def elementAt(self, i: int, j: int) -> str:
		return "1" if i == j else "0"

class DiagMatrix(Matrix):
	def elementAt(self, i: int, j: int) -> str:
		if i != j: return "0"

		rowIdx: str = self.lastRow if (self.lastRow and i == self.rowsNumber) else str(i)
		colIdx: str = self.lastCol if (self.lastCol and j == self.colsNumber) else str(j)

		return f"{self.element}_{{{rowIdx}{colIdx}}}" if self.generic else str(i*j)

class TriuMatrix(Matrix):
	def elementAt(self, i: int, j: int) -> str:
		if i + self.diagShift > j: return "0"

		rowIdx: str = self.lastRow if (self.lastRow and i == self.rowsNumber) else str(i)
		colIdx: str = self.lastCol if (self.lastCol and j == self.colsNumber) else str(j)

		return f"{self.element}_{{{rowIdx}{colIdx}}}" if self.generic else str(i*j)

class TrilMatrix(Matrix):
	def elementAt(self, i: int, j: int) -> str:
		if i - self.diagShift < j: return "0"

		rowIdx: str = self.lastRow if (self.lastRow and i == self.rowsNumber) else str(i)
		colIdx: str = self.lastCol if (self.lastCol and j == self.colsNumber) else str(j)

		return f"{self.element}_{{{rowIdx}{colIdx}}}" if self.generic else str(i*j)
	
class CustomMatrix(Matrix):
	elements = list()

	def elementAt(self, i: int, j: int) -> str:
		return self.elements[(i-1) * self.colsNumber + (j-1)]
	
	def setCustomElementsList(self, elements):
		self.elements = elements

class ZeroMatrix(Matrix):
	def elementAt(self, i: int, j: int) -> str:
		return "0"

class OnesMatrix(Matrix):
	def elementAt(self, i: int, j: int) -> str:
		return "1"


class MatrixShape(Enum):
	"""
	This enum maps each shaped-matrix class with its short name.
	For example a triangular upper matrix is called "triu" for short. By accessing the enum
	with its dictionary interface (MatrixShape["triu"]) you can retrieve the corresponding class
	that when istantiated will provide the proper elementAt method.
	To istantiate the class from the enum value, use the .value property.
	"""
	full = FullMatrix
	zeros = ZeroMatrix
	ones = OnesMatrix
	eye = EyeMatrix
	diag = DiagMatrix
	triu = TriuMatrix
	tril = TrilMatrix
	custom = CustomMatrix


def main(
	rowsNumber: str,
	colsNumber: str,
	elementName: str,
	generic: bool,
	compactRows: bool,
	compactCols: bool,
	diagShift: int,
	shape: MatrixShape
	):

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

	ShapedMatrixClass = shape.value
	matrix = ShapedMatrixClass(rowsNumber, colsNumber, lastRowSymbol, lastColSymbol, elementName, generic, diagShift)
	
	if shape == MatrixShape.custom:
		if not compactRows and not compactCols:
			import tui
			matrix.setCustomElementsList(tui.startInteractiveScreen(rowsNumber, colsNumber))
		else:
			raise ValueError("Unknown matrix dimensions")

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

	parser.add_argument("-r", "--rows", help="Matrix rows number. Can be a letter if representing symbolic index.", type=str, default=None, required=True)
	parser.add_argument("-c", "--columns", help="Matrix columns number. Can be a letter if representing symbolic index.", type=str, default=None, required=True)
	
	matrixShapeSubparser = parser.add_subparsers(title="shapes", dest="shape", help="Define matrix shape", required=True)
	matrixShapeSubparser.add_parser("zeros", help="Generate null matrix of specified dimensions")
	matrixShapeSubparser.add_parser("ones", help="Generate a matrix full of ones")
	matrixShapeSubparser.add_parser("full", help="Generate full (complete) matrix")
	matrixShapeSubparser.add_parser("eye", help="Generate identity matrix")
	matrixShapeSubparser.add_parser("diag", help="Generate diagonal matrix")
	triuParser = matrixShapeSubparser.add_parser("triu", help="Generate upper triangular matrix")
	trilParser = matrixShapeSubparser.add_parser("tril", help="Generate lower triangular matrix")	
	matrixShapeSubparser.add_parser("custom", help="Interactive screen to fill in the matrix your own way")	

	triuParser.add_argument("-d", "--diagonal-shift",
	help="Shift main diagonal to the d-th diagonal of the matrix."
	"Can be either a positive (shift diagonal towards the zeros) or a negative integer (shift towards the scalars).", type=int, default=0)

	trilParser.add_argument("-d", "--diagonal-shift",
	help="Shift main diagonal to the d-th diagonal of the matrix."
	"Can be either a positive (shift diagonal towards the zeros) or a negative integer (shift towards the scalars).", type=int, default=0)

	args = parser.parse_args()

	try:
		args.diagonal_shift
	except AttributeError as e:
		args.diagonal_shift = 0

	main(args.rows, args.columns, args.symbol, args.generic, args.compact_rows, args.compact_cols, args.diagonal_shift or 0, MatrixShape[args.shape])
