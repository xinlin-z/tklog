#!/usr/bin/env python3
import tkinter as tk
from tkinter import Toplevel, PhotoImage
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import asksaveasfilename
import logging
import threading
from collections import deque
import time


__VER = 'V0.13'


"""
About the SYNC argument in log interfaces (added in V0.12):

You should be VERY VERY careful to decide setting sync=True, since
it is very often to end up with dead lock. Normally, it only should
be set in background thread. You can not set sync=True in the event
loop of GUI!!
"""
class tklog(ScrolledText):
    """readonly scrolled text log class"""

    def __init__(self, **kw):
        super().__init__(**kw, state=tk.DISABLED, cursor='plus',
                         wrap=tk.WORD, font=('monospace',12))
        self.tag_config('TITLE', foreground='blue')
        self.tag_config('INFO', foreground='black')
        self.tag_config('DEBUG', foreground='gray')
        self.tag_config('WARNING', foreground='hotpink')
        self.tag_config('ERROR', foreground='red')
        self.tag_config('CRITICAL', foreground='red', underline=1)
        self.rpop = tk.Menu(self, tearoff=0)
        self.rpop.add_command(label='Export', command=self._copyas)
        self.rpop.add_command(label='Copy', command=self._copyto)
        self.rpop.add_command(label='Clear', command=self.clear)
        self.autoscroll = tk.IntVar(value=1)
        self.rpop.add_checkbutton(label='Autoscrolling',
                                  command=None,
                                  variable=self.autoscroll)
        self.editable = tk.IntVar(value=0)
        self.rpop.add_checkbutton(label='Editable',
                                  command=self._editable,
                                  variable=self.editable)
        self.bind('<Button-3>', self._popup)
        self.bind('<Button-1>', self._popdown)
        self.bind('<Up>', self._lineUp)
        self.bind('<Down>', self._lineDown)
        self.pList = []
        self.q = deque()
        self.stop = 0
        threading.Thread(target=self._writer, args=(), daemon=True).start()

    def destroy(self):
        self.stop = 1

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
        except tk.TclError:
            pass  # skip TclError while no selection
        else: self.clipboard_append(selection)

    def _editable(self):
        if self.editable.get():
            self.config(state=tk.NORMAL)
        else:
            self.config(state=tk.DISABLED)

    def _chState(self, state):
        if self.editable.get():
            return
        if state == 'on':
            self.config(state=tk.NORMAL)
        else:
            self.config(state=tk.DISABLED)

    def _writer(self):
        while True:
            if self.stop:
                break
            try:
                info = self.q.popleft()
            except IndexError:
                time.sleep(0.5)
                continue
            if isinstance(info, threading.Event):
                info.set()
                continue
            try:
                pos = info[:9].find('@')
                self._chState('on')
                if pos != -1:
                    if info[:pos] == 'CLEAR':
                        self.delete('1.0', tk.END)
                        self.pList = []
                        self.q.clear()
                    elif info[:pos] == 'PNG' or info[:pos] == 'GIF':
                        try:
                            self.pList.append(PhotoImage(file=info[pos+1:]))
                            self.image_create(tk.END, image=self.pList[-1])
                            self.insert(tk.END, '\n', 'DEBUG')
                        except Exception as e:
                            self.insert(tk.END, repr(e)+'\n', 'DEBUG')
                    else:
                        self.insert(tk.END, info[pos+1:], info[:pos])
                else:
                    self.insert(tk.END, '[undefined format]: '+info)
                self._chState('off')
                if self.autoscroll.get() == 1:
                    self.see(tk.END)
            except tk.TclError:
                break

    def _log(self, level, content, end, sync):
        self.q.append(level+'@'+content+end)
        if sync:
            self._syn_log()

    def _syn_log(self):
        wait2go = threading.Event()
        self.q.append(wait2go)
        wait2go.wait()

    def title(self, content, end='\n', *, sync=False):
        self._log('TITLE', content, end, sync)

    def info(self, content, end='\n', *, sync=False):
        self._log('INFO', content, end, sync)

    # directly call info will raise, why?
    log = info

    def debug(self, content, end='\n', *, sync=False):
        self._log('DEBUG', content, end, sync)

    def warning(self, content, end='\n', *, sync=False):
        self._log('WARNING', content, end, sync)

    def error(self, content, end='\n', *, sync=False):
        self._log('ERROR', content, end, sync)

    def critical(self, content, end='\n', *, sync=False):
        self._log('CRITICAL', content, end, sync)

    def png(self, pngFile, *, sync=False):
        self._log('PNG', pngFile, '', sync)

    def gif(self, gifFile, *, sync=False):
        self._log('GIF', gifFile, '', sync)

    def _lineUp(self, event):
        self.yview('scroll', -1, 'units')

    def _lineDown(self, event):
        self.yview('scroll', 1, 'units')

    def clear(self):
        self.q.append('CLEAR@')


class winlog():
    """readonly modaless Toplevel log window class"""

    def __init__(self, root, title='tklog window',
                             withdrawRoot=True,
                             destroyRoot=True):
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


