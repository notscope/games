import curses

def main(stdscr):
    stdscr.clear()
    stdscr.addstr("Press keys (ESC to exit):\n")

    while True:
        key = stdscr.getch()
        if key == 27:  # ESC key
            break
        stdscr.addstr(f"Key pressed: {chr(key) if key < 256 else key}\n")
        stdscr.refresh()

curses.wrapper(main)