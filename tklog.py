import tkinter as tk
from tkinter import Toplevel, PhotoImage
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import asksaveasfilename
import logging
import threading


class tklog(ScrolledText):
    """readonly scrolled text log class"""

    def __init__(self, **kw):
        super().__init__(**kw, state=tk.DISABLED, cursor='plus',
                               wrap=tk.WORD, font=('monospace',12))
        self.tag_config('TITLE', foreground='blue')
        self.tag_config('INFO', foreground='black')
        self.tag_config('DEBUG', foreground='gray')
        self.tag_config('WARNING', foreground='orange')
        self.tag_config('ERROR', foreground='red')
        self.tag_config('CRITICAL', foreground='red', underline=1)
        self.rpop = tk.Menu(self, tearoff=0)
        self.rpop.add_command(label='Export', command=self._copyas)
        self.rpop.add_command(label='Copy', command=self._copyto)
        self.rpop.add_command(label='Clean', command=self.clean)
        self.bind('<Button-3>', self._popup)
        self.bind('<Button-1>', self._popdown)
        self.bind('<Up>', self._lineUp)
        self.bind('<Down>', self._lineDown)
        # png and gif interface need call _log, so use RLock
        self.mutex = threading.RLock()
        self.pList = []

    def _popup(self, event):
        self.rpop.post(event.x_root, event.y_root)

    def _popdown(self, event):
        self.rpop.unpost()
        self.focus_set()

    def _copyas(self):
        saveTo = asksaveasfilename()
        if not isinstance(saveTo, str): return
        if saveTo == '': return
        with open(saveTo, 'w') as f:
            f.write(self.get('1.0', tk.END))

    def _copyto(self):
        self.clipboard_clear()
        try:
            selection = self.get(tk.SEL_FIRST, tk.SEL_LAST)
        except:
            pass  # skip TclError while no selection
        else: self.clipboard_append(selection)

    def _log(self, level, content, end):
        self.mutex.acquire()
        self.config(state=tk.NORMAL)
        self.insert(tk.END, content+end, level)
        self.config(state=tk.DISABLED)
        self.mutex.release()
        self.see(tk.END)

    def title(self, content, end='\n'):
        self._log('TITLE', content, end)

    def info(self, content, end='\n'):
        self._log('INFO', content, end)

    # directly call info will raise, why?
    log = info

    def debug(self, content, end='\n'):
        self._log('DEBUG', content, end)

    def warning(self, content, end='\n'):
        self._log('WARNING', content, end)

    def error(self, content, end='\n'):
        self._log('ERROR', content, end)

    def critical(self, content, end='\n'):
        self._log('CRITICAL', content, end)

    def png(self, pngFile):
        try:
            self.mutex.acquire()
            self.pList.append(PhotoImage(file=pngFile))
            self.image_create(tk.END,
                              image=self.pList[len(self.pList)-1])
            self.log('')
        except Exception as e:
            self.debug(repr(e))
        finally:
            self.mutex.release()

    def gif(self, gifFile):
        try:
            self.mutex.acquire()
            self.pList.append(PhotoImage(file=gifFile))
            self.image_create(tk.END,
                              image=self.pList[len(self.pList)-1])
            self.log('')
        except Exception as e:
            self.debug(repr(e))
        finally:
            self.mutex.release()

    def _lineUp(self, event):
        self.yview('scroll', -1, 'units')

    def _lineDown(self, event):
        self.yview('scroll', 1, 'units')

    def clean(self):
        self.config(state=tk.NORMAL)
        self.delete('1.0', tk.END)
        self.pList.clear()
        self.config(state=tk.DISABLED)


class tklogHandler(logging.Handler):
    """tklog handler inherited from logging.Handler"""

    def __init__(self, **kw):
        logging.Handler.__init__(self)
        self.tklog = tklog(**kw)

    def emit(self, record):
        if record.levelno== logging.DEBUG:
            self.tklog.debug(self.format(record))
        if record.levelno== logging.INFO:
            self.tklog.log(self.format(record))
        if record.levelno== logging.WARNING:
            self.tklog.warning(self.format(record))
        if record.levelno== logging.ERROR:
            self.tklog.error(self.format(record))
        if record.levelno== logging.CRITICAL:
            self.tklog.critical(self.format(record))

    def title(self, msg):
        self.tklog.title(msg)

    def png(self, pngFile):
        self.tklog.png(pngFile)

    def gif(self, gifFile):
        self.tklog.gif(gifFile)

    def pack(self, **kw):
        self.tklog.pack(**kw)

    def grid(self, **kw):
        self.tklog.grid(**kw)


class winlog():
    """readonly modaless Toplevel log window class"""

    def __init__(self, root, title='Log Window', withdrawRoot=True,
                    destroyRoot=True):
        self.root = root
        if withdrawRoot:
            self.root.withdraw()
        self.win = Toplevel(root)
        self.win.title(title)
        self.win.geometry('800x600')
        self.frame_0 = tk.Frame(self.win)
        self.frame_0.pack(fill='both', expand=True)
        self.st = tklog(master=self.frame_0, height=0)
        self.st.pack(fill='both', expand=True)
        self.frame_1 = tk.Frame(self.win)
        self.frame_1.pack(fill=tk.X)
        self.top = tk.Button(self.frame_1, text='Pin', command=self._pin)
        self.top.pack(side=tk.LEFT, padx=2, pady=2)
        self.win.bind('<FocusIn>', self._focusIn)
        self.win.bind('<FocusOut>', self._focusOut)
        self.pin = 0  # default is unpinned
        self.win.protocol('WM_DELETE_WINDOW', self.destroy)
        self.destroyRoot = destroyRoot

    def _focusIn(self, event):
        self.win.attributes('-alpha', 1.0)

    def _focusOut(self, event):
        self.win.attributes('-alpha', 0.7)

    def _pin(self):
        if self.pin == 0:
            self.win.attributes('-topmost', True)
            self.pin = 1
            self.top['text'] = 'Unpin'
        elif self.pin == 1:
            self.win.attributes('-topmost', False)
            self.pin = 0
            self.top['text'] = 'Pin'

    def title(self, content, end='\n'):
        self.st.title(content, end)

    def info(self, content, end='\n'):
        self.st.log(content, end)

    log = info

    def debug(self, content, end='\n'):
        self.st.debug(content, end)

    def warning(self, content, end='\n'):
        self.st.warning(content, end)

    def error(self, content, end='\n'):
        self.st.error(content, end)

    def critical(self, content, end='\n'):
        self.st.critical(content, end)

    def png(self, pngFile):
        self.st.png(pngFile)

    def gif(self, gifFile):
        self.st.gif(gifFile)

    def destroy(self):
        self.win.destroy()
        if self.destroyRoot:
            self.root.destroy()


class winlogHandler(logging.Handler):
    """winlog handler inherited from logging.Handler"""

    def __init__(self, **kw):
        logging.Handler.__init__(self)
        self.winlog = winlog(**kw)

    def emit(self, record):
        if record.levelno== logging.DEBUG:
            self.winlog.debug(self.format(record))
        if record.levelno== logging.INFO:
            self.winlog.log(self.format(record))
        if record.levelno== logging.WARNING:
            self.winlog.warning(self.format(record))
        if record.levelno== logging.ERROR:
            self.winlog.error(self.format(record))
        if record.levelno== logging.CRITICAL:
            self.winlog.critical(self.format(record))

    def title(self, msg):
        self.winlog.title(msg)

    def png(self, pngFile):
        self.winlog.png(pngFile)

    def gif(self, gifFile):
        self.winlog.gif(gifFile)


