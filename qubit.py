#!/usr/bin/env python3

def qubit(state):
    """Get the Ket-Bra notation representation of state"""

    return f"\\vert{state}\\rangle"

if __name__ == "__main__":
    state = input()
    print(qubit(state))