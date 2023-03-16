#!/usr/bin/env python3

import clipboard

def main():
    generated_latex = input()
    clipboard.copy(generated_latex)

if __name__ == "__main__":
    main()




