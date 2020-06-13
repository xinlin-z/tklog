import tkinter as tk
from tklog import tklogHandler
import logging


if __name__ == '__main__':
    root = tk.Tk()
    root.title('tklogHandler class show')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter('%(asctime)s: %(message)s')
    tkhandler = tklogHandler(master=root)
    tkhandler.pack(fill='both', expand=True, side=tk.RIGHT)
    tkhandler.setFormatter(fmt)
    logger.addHandler(tkhandler)
    logger.debug('this is debug')
    logger.info('this is info')
    logger.warning('this is warning')
    logger.error('this is error')
    logger.critical('this is critical')
    logger.title = tkhandler.title
    logger.png = tkhandler.png
    logger.gif = tkhandler.gif
    logger.title('this is title, can only be called by tklogHandler.')
    logger.png('pynote.net.png')
    logger.gif('funny.gif')
    root.mainloop()
