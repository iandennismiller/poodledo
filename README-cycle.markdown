Introduction
============
`cycle` is a command-line tool which implements the **Cycle System** from [Time Management for System Administrators](http://www.amazon.com/Management-System-Administrators-Thomas-Limoncelli/dp/0596007833) by Thomas Limoncelli. The Cycle System, in this context, has five main activities:

- Display the tasks assigned to today's list
- Add a new task
- Complete a task
- Move a task
- Reprioritize a task

It's a lot to explain in a short blurb here, but basically, the idea is to assign your tasks to a specific day, and by the end of the day, to have taken some action with each task (either completing it, deleting it, or moving it to another specific day). `cycle` implements this system by keying off of the `duedate` field in Toodledo; when you run `cycle` by itself, it will show a list of all of your tasks which have a `duedate` of today, along with their priorities. Really though, if this sounds at all intriguing, you should read the book; Tom explains it a lot better than I ever could.

Requirements
============
- Python 2.5+ (or, an older version with the ElementTree module installed)
- [Plex](http://www.cosc.canterbury.ac.nz/greg.ewing/python/Plex/) v2.0.0 (installable by pip)
- [parsedatetime](http://code.google.com/p/parsedatetime/) v0.8.7 (installable by pip)

Usage
=====
Running `cycle` by itself lists the tasks which are due today:

    $ ./cycle
    1: (A) Write README for cycle

`cycle -d` lists the tasks due on a specific day:

    $ ./cycle -d tuesday
    1: (D) Tuesday's demonstration task

This uses the [parsedatetime](http://code.google.com/p/parsedatetime/) library, which understands most human-readable strings ("tomorrow", "next wednesday", "june 12", etc.).

`cycle -a` adds a new task, due today:

    $ ./cycle -a Create a demonstration task
    $ ./cycle
    1: (A) Write README for cycle
    2: (D) Create a demonstration task

`cycle -p` reprioritizes a task:

    $ ./cycle -p 2 B
    Reprioritizing task 'Create a demonstration task' to B
    $ ./cycle
    1: (A) Write README for cycle
    2: (B) Create a demonstration task

`cycle -m` moves a task to another day (tomorrow by default):

    $ ./cycle -m 2
    Moving task 'Create a demonstration task' to tomorrow
    $ ./cycle -d tomorrow
    1: (B) Create a demonstration task

`cycle -c` marks a task as complete:

    $ ./cycle -c 1
    Marking task 'Write README for cycle' as complete

Notes
=====
- In order to use this script, you will need to [get your own API token](http://api.toodledo.com/2/account/doc_register.php). I have not included mine in the code. Add it to `ApiClient.__init__`.
- Pull requests always welcome!

License
=======
`cycle` is released under a **BSD License**. See the LICENSE file for details.

Contact
=======
You can email me at comptona@gmail.com.

To report bugs or request features, please use the **[Issues](https://github.com/handyman5/poodledo/issues)** feature.
