NEWS
====
2011-11-11
----------
I did some work to fix [Issue#2](https://github.com/handyman5/poodledo/issues/2):

- Configuration moved to `~/.tdcli/tdclirc`.
- To improve startup speed, `tdcli` caches a Python "pickle" of the lexer in `~/.tdcli/lexer.pickle`. This saves `tdcli` from having to regenerate the entire lexer each time. This file is safe to delete at any time; `tdcli` will just regenerate it the next time it's run.

I did not write code to automatically migrate the configuration file from the old location, so please keep in mind that you'll need to move it yourself.

2011-10-10
----------
I've made a few more improvements to the `tdcli` tool:

- `tdcli` now supports listing tasks with `-l` / `--list`
- `tdcli` now stores session and login data in `~/.tdclirc` instead of a file called "config" in the current directory

The next improvements I want to make are to have the list of tasks accept some filters (so I can say, "list all tasks with the tag 'work'"), and also to automatically list subtasks under their parents if your account supports them. Further on I'd like to implement more of the featureset of [the Ruby toodledo client](http://toodledo.rubyforge.org/toodledo/), specifically the "online" mode where you can poke around in your tasks and create folders, contexts, etc.

2011-10-03
----------
I made some significant improvements to the `tdcli` tool:

- Much better handling of the "config" file; in particular, if no valid session key or credentials are specified, it will ask for such on the command line, get a session key, and then cache the key (but not the credentials). This way, you don't have to store your password in plaintext anywhere.
- Added usage statement to tdcli to explain how the lexer works:

        $ tdcli -h
        Enter a task and associated metadata:

        context: @<context>
        due date: #<date>; toodledo parses dates smartly, including "#next thursday"
        due time: =<time>; translates time smartly
        folder: *<name>
        goal: +<goal>
        length: ~<time>; like "~4hours"
        location: -<location>
        note: ?<note data>
        priority: default is zero; single ! = 1, !! = 2, !!! = 3 (top)
        reminder: :<lead time>; ":5 hours"
        repeat: &<schedule>
        star: * alone makes the task starred
        start date: ><date> (&lt;)
        start time: ^<time>
        status: $<status>
        tag: %<tag>; can select multiple with "%tag1, tag2"

- And in non-tdcli news, I fixed a couple of bugs elsewhere in the code.

As of today, `tdcli` should be able to meet all of my command-line-task-adding needs; if there's something else you'd like it to do, please open a new issue or submit a pull request.

2011-08-28
----------
I've added a few new features to the library:

- Pretty-printing for ToodledoData objects (tasks and such)
- Smarter object detection and parsing for API client calls; now you can call "addTask('task name', folder='folder name')" and the folder ID will be figured out automatically
- And the biggie: parsing [the Toodledo email syntax](https://www.toodledo.com/info/help_email.php) for adding new tasks!

There is now a lexer.parse() function that will accept a string with the Toodledo email syntax and return a parsed task dictionary which addTask() will happily accept.

The new program `tdcli` demonstrates this feature:

    $ tdcli
    Enter a task description: This task is important !! #Today $Next Action

    modified: 1314577488
    id: 36647367
    title: This task is important
    priority: 2
    duedate: 1314532800
    status: 1
    added: 1314532800

Not all of the syntax options work yet, and the parsing is very fragile, so if you run into any trouble please submit an issue request.

------

Introduction
============
poodledo is a Python library for working with the web-based task management software [Toodledo](http://www.toodledo.com).

This particular version is an amalgam of two previous versions ([Felix Riedel's](http://code.google.com/p/poodledo/) and [Martin Treusch von Buttlar's](https://github.com/martint17r/poodledo)), substantially rewritten to use the [Toodledo API v2.0](http://api.toodledo.com/2/index.php).

Requirements
============
- Python 2.5+ (or, an older version with the ElementTree module installed)

Usage
=====
poodledo handles almost all of the API calls described in the [Toodledo docs](http://api.toodledo.com/2/index.php).

Initialization
--------------

Create an `ApiClient` object and call `authenticate()` to get a session key. This key is re-used in subsequent API calls until it expires.

    from apiclient import ApiClient
    c = ApiClient()
    c.authenticate('username@email.dom', 'password')

API Structure
-------------
Toodledo's API is broken down into six basic object types:

- Folders
- Contexts
- Goals
- Locations
- Notebooks
- Tasks

along with several other miscellaneous methods (`getAccountInfo`, `getToken`, etc.).

Each object type supports the same basic operations: "add", "delete", "edit", and "get". I'll use Folders for these examples, but the other object types have equivalent methods with the appropriate names (i.e., `getContexts`, `editLocation`, `deleteGoal`, etc.).

Retrieving
----------
Call `getFolders` to retrieve a list of folder objects from the API. This list is cached by the ApiClient until a change is made with another API call.

    c.getFolders()

Call `getFolder` to retrieve a specific folder object. This method takes one argument, which can be either the object's ID or its name/title.

    c.getFolder('My name is')
    c.getFolder(3472958)

Adding
------
Call `addFolder` to add a new folder with the API.

    c.addFolder('New Folder Name')

You can also specify object parameters as keyword arguments.

    c.addFolder('Private, Archived Folder', archived=True, private=True)

Deleting
--------
Call `deleteFolder` to delete a folder with the API. This method uses `getFolder` to identify its argument, so you can specify either the folder's name or its ID.

    c.deleteFolder('Doomed Folder')

Editing
-------
Call `editFolder` to change a folder's characteristics. Use the same arguments as `getFolder` to identify the target, and pass the changes as keyword arguments.

    c.editFolder('Current Folder Name', name='New Folder Name', private=True)

Notes
=====
- In order to use this library, you will need to [get your own API token](http://api.toodledo.com/2/account/doc_register.php). I have not included mine in the code. Add it to `ApiClient.__init__`.
- The test harness `test_poodledo.py` does not function at all currently.
- Pull requests always welcome!

TODO
====
- Update the test harness `test_toodledo.py` for API 2.0
- Implement a generic account/key storage system
- Write several sample scripts for reference
- Add batch processing for notes and tasks
- Write a "pythonic" wrapper that makes the returned objects smart (e.g., doing `task_object.name = "New Name"` would actually update the task's name with the API)
- Make objects which have an ordering (folders and subtasks) a) honor that ordering, and b) be re-orderable

License
=======
poodledo is released under a **BSD License**. See the LICENSE file for details.

Contact
=======
You can email me at comptona@gmail.com.

To report bugs or request features, please use the **[Issues](https://github.com/handyman5/poodledo/issues)** feature.
