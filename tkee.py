import sys
import tkinter as tk
import threading
from tklog import winlog


def readlog(log):
    while True:
        line = sys.stdin.readline()
        if line:
            print(line, end='')
            log.log(line, end='')
        else:
            break


if __name__ == '__main__':
    root = tk.Tk()
    log = winlog(root)
    threading.Thread(target=readlog,args=(log,),daemon=True).start()
    root.mainloop()
