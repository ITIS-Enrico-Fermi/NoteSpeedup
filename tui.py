#!/usr/bin/env python3

import urwid
from typing import *


def onExitClick(button: urwid.Button) -> NoReturn:
  raise urwid.ExitMainLoop()

def onGenerateClick(res: urwid.Text, button: urwid.Button) -> NoReturn:
  res.set_text("test")
  raise urwid.ExitMainLoop()


class Grid(urwid.Pile):
  def __init__(self, rows: int, cols: int, cellSize: int = 7):
    div = urwid.Divider()
    cell = (cellSize, urwid.LineBox(urwid.Edit("", align="center")))
    
    row = urwid.Columns(
      [div] +
      [cell for c in range(cols)] +
      [div]
    )

    super(Grid, self).__init__([row for r in range(rows)])

def main() -> None:
  resTxt = urwid.Text(u"")
  headerTxt = urwid.Text(u"Fill the matrix with coefficients or scalars by moving with arrow keys.\nClick on GENERATE to quit this interactive screen and print the result on stdout.")

  exitButton = urwid.Button(u"EXIT")
  urwid.connect_signal(exitButton, "click", onExitClick)
  
  generateButton = urwid.Button(u"GENERATE")
  urwid.connect_signal(generateButton, "click", onGenerateClick, user_args=[resTxt])

  div = urwid.Divider()
  buttonsList = urwid.Columns([
    div,
    (8, exitButton),
    (5, div),
    (12, generateButton)
  ])

  grid = Grid(3, 4)
  frame = urwid.Frame(urwid.Filler(grid), header=headerTxt, footer=buttonsList, focus_part="footer")
  frame.set_focus("body")

  urwid.MainLoop(frame).run()
  print(resTxt.get_text()[0])

if __name__ == "__main__":
  main()