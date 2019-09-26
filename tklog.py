import tkinter as tk
from tkinter import Toplevel
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import asksaveasfilename


# in Win system, the default font is too ugly.
_font = ('monospace',12)


class tklog(ScrolledText):
    """readonly scrolled text log class"""

    def __init__(self, **kw):
        super().__init__(**kw,state=tk.DISABLED,cursor='plus',
                            wrap=tk.WORD,font=_font)
        self.tag_configure('red', foreground='red')
        self.tag_configure('blue', foreground='blue')
        self.rpop = tk.Menu(self, tearoff=0)
        self.rpop.add_command(label='Export all to file',command=self._copyas)
        self.rpop.add_command(label='Copy to clipboard',command=self._copyto)
        self.bind('<Button-3>', self._popup)
        self.bind('<Button-1>', self._popdown)
        self.bind('<Up>', self._lineUp)
        self.bind('<Down>', self._lineDown)
        self.focus_set()  # !

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

    def log(self, content, end='\n'):
        self.config(state=tk.NORMAL)
        self.insert(tk.END, content+end)
        self.see(tk.END)
        self.config(state=tk.DISABLED)

    def warning(self, content, end='\n'):
        self.config(state=tk.NORMAL)
        self.insert(tk.END, content+end, 'blue')
        self.see(tk.END)
        self.config(state=tk.DISABLED)
        
    def error(self, content, end='\n'):
        self.config(state=tk.NORMAL)
        self.insert(tk.END, content+end, 'red')
        self.see(tk.END)
        self.config(state=tk.DISABLED)

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

    def __init__(self, root=None, title='Log Window', **kw):
        self.win = Toplevel(root)
        self.win.title(title)
        self.st = tklog(master=self.win, **kw)
        self.st.pack(fill='both', expand=True)

    def log(self, content, end='\n'):
        self.st.log(content, end)

    def warning(self, content, end='\n'):
        self.st.warning(content, end)

    def error(self, content, end='\n'):
        self.st.error(content, end)

    def destroy(self):
        self.win.destroy()


if __name__ == '__main__':  # test code
    root = tk.Tk()
    eblog=  tklog(master=root)
    eblog.pack()
    eblog.log('this log text widget is created by tklog class')
    eblog.log('I am on root window')
    eblog.log('this is log')
    eblog.warning('this is warning')
    eblog.error('this is error')
    wlog = winlog(root, 'test winlog class', width=48)
    wlog.log('this modaless log window is created by winlog class')
    wlog.log('I am a modaless window based on root')
    wlog.log('this is log')
    wlog.warning('this is warning')
    wlog.error('this is error')
    import textwrap
    wlog.log(textwrap.dedent("""\
    In these objects, click right button of your mouse, you can get two 
    useful options, Export all to file and Copy to clipboard. 
    The text area will always be readonly, you don't need to worry that 
    log info would be broken by any reasons. Have fun...
    
    Please don't save your star:
    https://github.com/xinlin-z/tklog

    welcome to my blogs:
    https://www.pynote.net
    https://www.maixj.net
    """))
    root.mainloop()


