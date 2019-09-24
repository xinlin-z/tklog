# tklog
a handy log widget based on tkinter


Log is just like a cup of Latte, and I like it anytime.


When you are hacking a GUI program with tkinter, maybe the console is closed.
You can not use print to log easily. By using tk.Text or scrolledtext widget
is good choice, and anyway here I give you a "better" alternative: tklog.


There are two classes in tklog.py: (1) tklog, (2) winlog.


**tklog class** can be used anywhere in GUI window, it's an enhanced scrolledtext
widget (from Python standard libary) which added to response Up and Donw key 
press, **right click will open a menu that gives you two options: 
(1) Export all to file, (2) Copy to clipboard. **


**winlog class** is a modaless toplevel window by using tklog, that's all.


All text area is readonly, and so you do not need to worry that the log 
information would be broken by any reasons. 


**中文参考： https://www.pynote.net/archives/1207**

## interfaces for tklog

    tklog.log  # log in black
    tklog.waring  # log in blue
    tklog.error  # log in red
    tklog.clean  # clean all log info
    
## interfaces for winlog

    winlog.log
    winlog.warning
    winlog.error
    winlog.destroy  # self destroy
    
## test code

    $ python3 tklog.py
 
 
 This is what you should expected:
![tklog](https://www.pynote.net/pics/uploads/2019/09/run_tklog.py_.jpg)
