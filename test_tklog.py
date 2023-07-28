import sys
import tkinter as tk
from tklog import tklog, winlog
import time
import threading
import random


def _poster(log):
    while True:
        r = random.randint(1,8)
        log.log(time.strftime('%Y-%m-%d %H:%M:%S %A')
                +' '+str(threading.get_ident()))
        if r == 1:
            c = random.randint(1,8)
            if c == 1:
                log.debug('Test SYNC log..!!', sync=True)
            elif c == 2:
                log.log('Test SYNC log..!!', sync=True)
            elif c == 3:
                log.warning('Test SYNC log..!!', sync=True)
            elif c == 4:
                log.error('Test SYNC log..!!', sync=True)
            elif c == 5:
                log.critical('Test SYNC log..!!', sync=True)
            elif c == 6:
                log.title('Test SYNC log..!!', sync=True)
            elif c == 7:
                log.debug('sync gif...')
                log.gif('funny.gif', sync=True)
            else:
                log.debug('sync png...')
                log.png('ty.png', sync=True)
        elif r == 2:
            log.debug('log is just like a cup of coffee!')
        elif r == 3:
            log.error('secret error...@#$%$#@#$%')
        elif r == 4:
            log.warning('Bad news: tomorrow is not weekend...')
        elif r == 5:
            log.title('he is always playing games...')
        elif r == 6:
            log.critical('this is a critical situation!')
        elif r == 7:
            log.gif('funny.gif')
        else:
            log.png('ty.png')
        time.sleep(8/r)


if __name__ == '__main__':  # test code
    root = tk.Tk()
    if sys.argv[1] == 'winlog':
        log = winlog(root)
    else:
        root.title('test tklog')
        log = tklog(master=root)
        log.pack(fill='both', expand=True, side=tk.LEFT)
    log.log('insert a few log lines before mainloop...')
    log.log('insert a gif picture:')
    log.gif('funny.gif')
    log.debug('[debug] gif cannot move is a known issue!')
    log.log('insert a png picture:')
    log.png('ty.png')
    log.log('[log] gif cannot move is a known issue!')
    log.warning('[warning] gif cannot move is a known issue!')
    log.error('[error] gif cannot move is a known issue!')
    log.critical('[critical] gif cannot move is a known issue!')
    log.title('[title] gif cannot move is a knonw issue!')
    log.png('test_not_existed_pic.png')
    log.gif('test_not_existed_pic.gif')
    log.critical('start 7 test threads...')
    for i in range(7):
        threading.Thread(target=_poster, args=(log,), daemon=True).start()
    root.mainloop()

