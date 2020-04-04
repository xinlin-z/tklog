# tklog
a handy log widget based on tkinter


Log is just like a cup of Latte, and I like it anytime.


When you are hacking a GUI program with tkinter, maybe the console is closed.
You can not use print to log easily. By using tk.Text or scrolledtext widget
is good choice, and anyway here I give you a "better" alternative: tklog.


There are two classes in tklog.py: 

(1) tklog, 

(2) winlog.


**tklog class** can be used anywhere in GUI window, it's an enhanced 
scrolledtext widget (from Python standard libary) which added to response Up 
and Donw key press, right click will open a menu that gives you 3 options: 

(1) Export (all to file), 

(2) Copy (selected to clipboard),

(3) Clean (all).


**winlog class** is a modaless toplevel window inherited from tklog. 


All text area is **readonly**, and so you do not need to worry that the log 
information would be broken by unexpected or careless operations. 


**中文参考： https://www.pynote.net/archives/1207**

# run test code

    $ python3 tklog.py

You'll see two windows show.
