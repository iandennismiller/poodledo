Current porting issues
----------------------

- Need to find an elegant way to use either items or iteritems, as appopriate
- the parsedatetime version in pip doesn't support python3 (although the version in github does)
- toodledodata struct uses "unicode"; need to figure out how to make this clean for "this should be a unicode string" in both ("unicode" wasn't added back until 3.2?)
