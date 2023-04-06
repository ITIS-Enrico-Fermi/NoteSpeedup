#!/usr/bin/env python3

import curses
import operator
from curses.textpad import Textbox, rectangle


def main(win: curses.window) -> None:
  WIN_MIDPOINT = (
    int(curses.COLS / 2),
    int(curses.LINES / 2)
  )
  MATRIX_SIZE = (
    5,
    5
  )
  MATRIX_MIDPOINT = tuple(
    map(
      operator.floordiv,
      MATRIX_SIZE,
      (2, 2)
    )
  )

  RECTANGLE_UL = tuple(
    map(
      operator.sub,
      WIN_MIDPOINT,
      MATRIX_MIDPOINT
    )
  )

  RECTANGLE_BR = tuple(
    map(
      operator.add,
      RECTANGLE_UL,
      MATRIX_SIZE
    )
  )

  win.clear()
  win.leaveok(True)
  rectangle(win, RECTANGLE_UL[1], RECTANGLE_UL[0], RECTANGLE_BR[1], RECTANGLE_BR[0])

  box = Textbox(win)
  box.edit(lambda key: key if chr(key).isnumeric() or chr(key).isalpha() else None)
  print(box.gather())

  # win.getkey()

if __name__ == "__main__":
  curses.wrapper(main)  # Creates stdscr, turns on cbreak, turns off echo, enables terminal keypad