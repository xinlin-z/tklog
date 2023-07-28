import tkinter as tk
import textwrap
from tklog import winlog


if __name__ == '__main__':
    root = tk.Tk()
    wlog = winlog(root, 'Test winlog class', True, True)
    wlog.title('winlog class intro:')
    wlog.log(textwrap.dedent("""\
            This modaless log window is created by winlog class, which is
            inherited from tklog class. So it has almost the same methods,
            except that it is floated."""))
    wlog.debug('debug info')
    wlog.warning('warning info')
    wlog.error('error info')
    wlog.critical('critical info')
    wlog.png('ty.png')
    wlog.gif('funny.gif')
    wlog.title('Have fun...')
    root.mainloop()
