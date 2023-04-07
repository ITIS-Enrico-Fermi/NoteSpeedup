#!/usr/bin/env python3

import urwid
from typing import *


GENERATE = False

class Grid(urwid.Pile):
  def __init__(self, rows: int, cols: int, cellSize: int = 7):
    self.cellsEditor = [urwid.Edit("", align="center") for i in range(rows*cols)]
    self.__rows = rows
    self.__cols = cols

    div = urwid.Divider()

    super(Grid, self).__init__([
      urwid.Columns(
        [div] +
        [
          (cellSize, urwid.LineBox(self.cellsEditor[r*cols+c])) for c in range(cols)
        ] +
        [div]
      ) for r in range(rows)
    ])
  
  
  def get_text(self, r: int, c: int) -> str:
    return self.cellsEditor[r*self.__cols+c].get_text()

class FocusManager:
  def __init__(self, frame: urwid.Frame):
    self.frame = frame

  def __call__(self, input: str) -> bool:
    if input == 'tab':
      self.frame.set_focus(
        "footer" if self.frame.get_focus() == "body"
        else "body"
      )
      return True
    return False


def onExitClick(button: urwid.Button) -> NoReturn:
  raise urwid.ExitMainLoop()

def onGenerateClick(button: urwid.Button) -> NoReturn:
  global GENERATE
  GENERATE = True
  raise urwid.ExitMainLoop()

def main() -> None:
  headerTxt = urwid.Text(u"Fill the matrix with coefficients or scalars by moving with arrow keys.\nClick on GENERATE to quit this interactive screen and print the result on stdout.")

  exitButton = urwid.Button(u"EXIT")
  urwid.connect_signal(exitButton, "click", onExitClick)
  
  generateButton = urwid.Button(u"GENERATE")
  urwid.connect_signal(generateButton, "click", onGenerateClick)

  div = urwid.Divider()
  buttonsList = urwid.Columns([
    div,
    (8, exitButton),
    (5, div),
    (12, generateButton)
  ])

  grid = Grid(3, 4)
  frame = urwid.Frame(urwid.Filler(grid), header=headerTxt, footer=buttonsList, focus_part="body")

  focusManager = FocusManager(frame)
  urwid.MainLoop(frame, unhandled_input = focusManager).run()

  if GENERATE:
    print(" ".join([
      editor.get_text()[0] for editor in grid.cellsEditor
    ]))

if __name__ == "__main__":
  main()