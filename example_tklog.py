import tkinter as tk
from tklog import tklog
import time
import threading


def _poster(log):
    while True:
        log.title('test sync log', sync=True)
        log.log(time.strftime('%Y-%m-%d %H:%M:%S %A'))
        log.debug('test autoscrolling option')
        time.sleep(2)
        log.error('test sync log', sync=True)


if __name__ == '__main__':  # test code
    import textwrap
    root = tk.Tk()
    root.title('tklog class show')
    # tklog class show
    eblog = tklog(master=root)
    eblog.pack(fill='both', expand=True, side=tk.LEFT)
    eblog.log(textwrap.dedent("""\
              This log widget in root window is created by tklog class.
              Suppose we have code below:
              >>> from tklog import tklog
              >>> root = tk.Tk()
              >>> eblog = tklog(master=root)
              >>> eblog.pack()
              # now we can call methods of eblog object"""))
    eblog.log('>>> eblog.title(\'this is title\')')
    eblog.title('this is title')
    eblog.log('>>> eblog.log(\'this is log\')')
    eblog.log('this is log')
    eblog.log('>>> eblog.debug(\'this is debug\')')
    eblog.debug('this is debug')
    eblog.log('>>> eblog.warning(\'this is warning\')')
    eblog.warning('this is warning')
    eblog.log('>>> eblog.error(\'this is error\')')
    eblog.error('this is error')
    eblog.log('>>> eblog.critical(\'this is critical\')')
    eblog.critical('this is critical')
    eblog.log('>>> eblog.png(\'./pynote.net.png\')')
    eblog.png('pynote.net.png')
    eblog.log('>>> eblog.gif(\'./funny.gif\')')
    eblog.gif('funny.gif')
    eblog.warning('gif cannot move is a known issue!')
    eblog.title('Have fun...')
    eblog.png('test_not_existed_pic.png')
    eblog.gif('test_not_existed_pic.gif')
    t = threading.Thread(target=_poster, args=(eblog,), daemon=True)
    t.start()
    root.mainloop()

