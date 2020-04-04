import tkinter as tk
from tkinter import Toplevel, PhotoImage
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import asksaveasfilename


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
        self.pngList = []

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

    def title(self, content, end='\n'):
        self.config(state=tk.NORMAL)
        self.insert(tk.END, content+end, 'TITLE')
        self.see(tk.END)
        self.config(state=tk.DISABLED)
    
    def log(self, content, end='\n'):  # the name 'info' is not allowed
        self.config(state=tk.NORMAL)
        self.insert(tk.END, content+end, 'INFO')
        self.see(tk.END)
        self.config(state=tk.DISABLED)

    def debug(self, content, end='\n'):
        self.config(state=tk.NORMAL)
        self.insert(tk.END, content+end, 'DEBUG')
        self.see(tk.END)
        self.config(state=tk.DISABLED)
    
    def warning(self, content, end='\n'):
        self.config(state=tk.NORMAL)
        self.insert(tk.END, content+end, 'WARNING')
        self.see(tk.END)
        self.config(state=tk.DISABLED)
        
    def error(self, content, end='\n'):
        self.config(state=tk.NORMAL)
        self.insert(tk.END, content+end, 'ERROR')
        self.see(tk.END)
        self.config(state=tk.DISABLED)

    def critical(self, content, end='\n'):
        self.config(state=tk.NORMAL)
        self.insert(tk.END, content+end, 'CRITICAL')
        self.see(tk.END)
        self.config(state=tk.DISABLED)

    def png(self, pngFile):
        try:
            self.pngList.append(PhotoImage(file=pngFile))
            self.image_create(tk.END, 
                              image=self.pngList[len(self.pngList)-1])
            self.log('\n', end='')
        except Exception as e: 
            self.debug(repr(e))
    
    def _lineUp(self, event):
        self.yview('scroll', -1, 'units')
         
    def _lineDown(self, event):
        self.yview('scroll', 1, 'units')

    def clean(self):
        self.config(state=tk.NORMAL)
        self.delete('1.0', tk.END)
        self.config(state=tk.DISABLED)


class winlog():
    """readonly modaless Toplevel log window class"""

    def __init__(self, root=None, title='Log Window'):
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
    
    def log(self, content, end='\n'):
        self.st.log(content, end)

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
    
    def destroy(self):
        self.win.destroy()


if __name__ == '__main__':  # test code
    import textwrap
    root = tk.Tk()
    root.title('tklog class show')
    # tklog class show
    eblog = tklog(master=root)
    eblog.pack(fill='both', expand=True)
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
    eblog.title('Have fun...')
    # winlog class show
    wlog = winlog(root, 'winlog class show')
    wlog.title('winlog class intro:')
    wlog.log(textwrap.dedent("""\
            This modaless log window is created by winlog class, which is 
            inherited from tklog class. So it has almost the same methods,
            except that it is floated."""))
    wlog.debug('debug info')
    wlog.warning('warning info')
    wlog.error('error info')
    wlog.critical('critical info')
    wlog.png('pynote.net.png')
    wlog.title('Have fun...')
    root.mainloop()


