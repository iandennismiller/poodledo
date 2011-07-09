Introduction
============
poodledo is a Python library for working with the web-based task management software [Toodledo](http://www.toodledo.com).

This particular version is an amalgam of two previous versions ([Felix Riedel's](http://code.google.com/p/poodledo/) and [Martin Treusch von Buttlar's](https://github.com/martint17r/poodledo)), substantially rewritten to use the [Toodledo API v2.0](http://api.toodledo.com/2/index.php).

Requirements
============
- Python 2.5+ (or, an older version with the ElementTree module installed)

Usage
=====

    from apiclient import ApiClient
    c = ApiClient()
    c.authenticate('username@email.dom', 'password')
    c.getFolders()  # etc.

Notes
=====
- In order to use this library, you will need to [get your own API token](http://api.toodledo.com/2/account/doc_register.php). I have not included mine in the code. Add it to `ApiClient.__init__`.
- The test harness `test_poodledo.py` does not function at all currently. Updating it for the 2.0 API is on my list.



License
=======
poodledo is released under a **BSD License**. See LICENSE file for details.


Contact
=======
You can email me at comptona@gmail.com.

To report bugs or request features, please use the **[Issues](https://github.com/handyman5/poodledo/issues)** feature.
