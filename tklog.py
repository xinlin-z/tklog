import tkinter as tk
from tkinter import Toplevel, PhotoImage
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import asksaveasfilename
import logging
import threading
import queue


# When too many threads put info in the queue, and there is only one
# thread to get and consume, a lot of info maybe stocked in the queue,
# and it needs so much time to get and consume them all. So, set a length
# to the queue to slow down all the crazy threads.
# But, there is another risk. If your GUI event handler put info directly,
# without in a thread, your program might be deadlock if the queue is not
# long enough.
# So, to be a little balance in between, here we go:
QUEUE_LEN = 2048
# And, put method is set with block=False.


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
        self.autoscroll = tk.IntVar(value=1)
        self.rpop.add_checkbutton(label='Autoscrolling',
                                  command=None,
                                  variable=self.autoscroll)
        self.bind('<Button-3>', self._popup)
        self.bind('<Button-1>', self._popdown)
        self.bind('<Up>', self._lineUp)
        self.bind('<Down>', self._lineDown)
        self.pList = []
        self.q = queue.Queue(QUEUE_LEN)
        self.stop = 0
        self.wt = threading.Thread(target=self._writer,
                                   args=(), daemon=True)
        self.wt.start()

    def destroy(self):
        self.stop = 1
        self.q.put(None)  # q.get is blocked, so we need put sth.

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

    def _writer(self):
        while True:
            info = self.q.get()
            if self.stop: break
            try:
                pos = info[:9].find('@')
                if pos == -1:
                    self.config(state=tk.NORMAL)
                    self.insert(tk.END, '[undefined format]: '+info)
                    self.config(state=tk.DISABLED)
                else:
                    if info[:pos] == 'CLEAN':
                        self.config(state=tk.NORMAL)
                        self.delete('1.0', tk.END)
                        self.config(state=tk.DISABLED)
                    elif info[:pos] == 'PNG' or info[:pos] == 'GIF':
                        try:
                            self.pList.append(PhotoImage(file=info[pos+1:]))
                            self.config(state=tk.NORMAL)
                            self.image_create(
                                    tk.END,
                                    image=self.pList[len(self.pList)-1])
                            self.insert(tk.END, '\n', 'DEBUG')
                            self.config(state=tk.DISABLED)
                        except Exception as e:
                            self.config(state=tk.NORMAL)
                            self.insert(tk.END, repr(e)+'\n', 'DEBUG')
                            self.config(state=tk.DISABLED)
                    else:
                        self.config(state=tk.NORMAL)
                        self.insert(tk.END, info[pos+1:], info[:pos])
                        self.config(state=tk.DISABLED)
                if self.autoscroll.get() == 1:
                    self.see(tk.END)
            except tk.TclError:
                break

    def _log(self, level, content, end):
        self.q.put(level+'@'+content+end, block=False)

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
        self.q.put('PNG@'+pngFile, block=False)

    def gif(self, gifFile):
        self.q.put('GIF@'+gifFile, block=False)

    def _lineUp(self, event):
        self.yview('scroll', -1, 'units')

    def _lineDown(self, event):
        self.yview('scroll', 1, 'units')

    def clean(self):
        self.q.put('CLEAN@', block=False)


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

    def __init__(self, root, title='Log Window', withdrawRoot=False,
                    destroyRoot=False):
        self.root = root
        if withdrawRoot:
            self.root.withdraw()
        self.win = Toplevel(root)
        self.win.title(title)
        self.win.geometry('600x800')
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


