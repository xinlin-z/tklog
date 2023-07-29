Log is just like a cup of coffee, and I like it anytime! :)

* [tklog](#tklog)
* [winlog](#winlog)
* [sample test code](#sample-test-code)
* [tkee](#tkee)

# tklog

**tklog:** a thread-safe log widget based on tkinter
(inherited from ScrolledText).

It can be packed into root or Toplevel window easily, and has a
little power to log pictures (png and gif).

The log interfaces all have an argument named sync from V0.12,
default is False. You should be very careful about this argument,
you can never use it in GUI event loop. Normally, `sync=True`
should only be set in background thread which needs synchronization.
For example, you want to make sure the log interface
would be blocked until after the log info is shown on text window.

# winlog

**winlog:** a toplevel log window based on tklog, which creats a
Toplevel window, contains a tklog widget, and has the ability to
withdraw or destroy root.

# sample test code

Read the sample test code, and you'll learn how to use tklog and
winlog. And you can also run the sample test code:

```python
$ python test_tklog.py tklog
$ python test_tklog.py winlog
```

Don't forget to try **right click** on the logging area. Maybe
there's a surprise for you.

Below is a screenshot for winlog:

![winlog.png](/winlog.png)

# tkee


