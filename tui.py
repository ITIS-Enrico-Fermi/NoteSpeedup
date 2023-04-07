#!/usr/bin/env python3

import urwid
from typing import *


def onExitClick(button: urwid.Button) -> NoReturn:
  raise urwid.ExitMainLoop()

def onGenerateClick(res: urwid.Text, button: urwid.Button) -> NoReturn:
  res.set_text("test")
  raise urwid.ExitMainLoop()

def main() -> None:
  resTxt = urwid.Text(u"")
  headerTxt = urwid.Text(u"Fill the matrix with coefficients or scalars by moving with arrow keys.\nClick on GENERATE to quit this interactive screen and print the result on stdout.")

  exitButton = urwid.Button(u"EXIT")
  urwid.connect_signal(exitButton, "click", onExitClick)
  
  generateButton = urwid.Button(u"GENERATE")
  urwid.connect_signal(generateButton, "click", onGenerateClick, user_args=[resTxt])

  buttonsList = urwid.Columns([exitButton, generateButton])

  filler = urwid.Filler(headerTxt, "top")
  frame = urwid.Frame(filler, header=headerTxt, footer=buttonsList, focus_part="footer")
  
  urwid.MainLoop(frame).run()
  print(resTxt.get_text()[0])

if __name__ == "__main__":
  main()