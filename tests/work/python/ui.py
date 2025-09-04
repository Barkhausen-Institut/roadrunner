import curses
import time

def main(screen):
    screen.clear()
    wnd = curses.newwin(5, 15, 5, 5)
    wnd.border()
    wnd.addstr(2, 4, "Hello !")
    wnd.refresh()
    time.sleep(1)
    for n in range(5, 0, -1):
        wnd.erase()
        wnd.border()
        wnd.addstr(2, 4, f"Wait {n}")
        wnd.refresh()
        time.sleep(1)

if __name__ == "__main__":
    curses.wrapper(main)
