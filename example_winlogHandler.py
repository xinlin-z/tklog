import tkinter as tk
from tklog import winlogHandler
import logging


if __name__ == '__main__':
    root = tk.Tk()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter('%(asctime)s: %(message)s')
    winhandler = winlogHandler(root=root,
                               title='winlogHandler class show',
                               withdrawRoot=True,
                               destroyRoot=True)
    winhandler.setFormatter(fmt)
    logger.addHandler(winhandler)
    logger.debug('this is debug')
    logger.info('this is info')
    logger.warning('this is warning')
    logger.error('this is error')
    logger.critical('this is critical')
    logger.title = winhandler.title
    logger.png = winhandler.png
    logger.gif = winhandler.gif
    logger.title('this is title, can only be called by winlogHandler.')
    logger.png('pynote.net.png')
    logger.gif('funny.gif')
    root.mainloop()
