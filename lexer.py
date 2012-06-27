from StringIO import StringIO
from cli import CONFIGDIR
from os.path import exists, join
from plex import *
from time import mktime
import parsedatetime.parsedatetime as pdt
import pickle

USAGE = '''Enter a task and associated metadata:

context: @<context>
due date: #<date>; toodledo parses dates smartly, including "#next thursday", and email does consume the space after #next as part of the date
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
'''

p = pdt.Calendar()

def build_lexer(picklefile=None):
    lex = None
    if picklefile and exists(picklefile):
        try:
            with open(picklefile, "r") as fd:
                lex = pickle.load(fd)
        except (KeyError, IOError):
            pass    # pickle loading failed; regenerate lexer

    if not lex:
        letter = Range("AZaz")
        digit = Range("09")
        apos = Str("'")
        dash = Str("-")
        comma = Str(",")
        period = Str(".")
        slash = Str("/")
        underscore = Str("_")
        parens = Any("()")
        formatting = Any("'-,./_():;?\\|!+#*%&")
        word = Rep1(letter | digit | parens | dash | slash) + Rep(letter | digit | apos | dash | comma | period | slash | underscore | formatting | parens)
        number = Rep1(digit)
        space = Any(" \t")
        newline = Any("\n\r")
        quote = Str("'")
        doublequote= Str('"')
        bolsp = Alt(Bol, space)
        freetext = Alt( Rep1(word) + Rep(space + word),
                        quote + Rep1(word) + Rep(space + word) + quote,
                        doublequote + Rep1(word) + Rep(space + word) + doublequote)

        folder = bolsp + Str("*") + Rep1(freetext)
        context = bolsp + Str("@") + Opt(Str("@")) + Rep1(freetext)
        excl = Str("!")
        priority = bolsp + Rep1(excl)
        star = bolsp + Str("*")
#datefield = digit + digit + digit + digit + Str("/", "-") + digit + digit + Str("/", "-") + digit + digit
        datefield = freetext
        duedate = bolsp + Str("#") + datefield
        startdate = bolsp + Str(">") + datefield
        goal = bolsp + Str("+") + Rep1(freetext)
        status = bolsp + Str("$") + Rep1(freetext)
#tagname = Rep1(word) + Opt(Str(",")) + Opt(space)
        tag = bolsp + Str("%") + Rep1(word) + Rep(Str(",") + Opt(space) + word)
        timefield = Rep1(number) + Opt(Str(":") + Rep1(number)) + Opt(space) + Str("AM", "PM", "am", "pm")
        duetime = bolsp + Str("=") + Rep1(timefield)
        starttime = bolsp + Str("^") + Rep1(timefield)
        location = bolsp + Str("-") + Rep1(freetext)
        durationfield = freetext
        length = bolsp + Str("~") + Rep1(durationfield)
        reminder = bolsp + Str(":") + Rep1(durationfield)
        anything = Rep1(letter | digit | formatting | bolsp)
        note = bolsp + Str("?") + Rep1(anything)

        lex = Lexicon([
                (space, IGNORE),
                (newline, 'newline'),
                (freetext, 'title'),
                (folder, 'folder'),
                (context, 'context'),
                (priority, 'priority'),
                (duedate, 'duedate'),
                (startdate, 'startdate'),
                (goal, 'goal'),
                (status, 'status'),
                (tag, 'tag'),
                (duetime, 'duetime'),
                (starttime, 'starttime'),
                (location, 'location'),
                (length, 'length'),
                (reminder, 'reminder'),
                (note, 'note'),
                ])

        if picklefile:
            with open(picklefile, "w") as fd:
                pickle.dump(lex, fd)

    return lex

def rationalize(task):
    for k in task.keys():
        task[k] = task[k].strip()
        if k in ['folder', 'context', 'duedate', 'startdate', 'goal', 'location', 'status', 'tag', 'duetime', 'starttime', 'length', 'reminder', 'note']:
            task[k] = task[k][1:]
        if task[k][0] == '"' and task[k][-1] == '"':
            task[k] = task[k][1:-1]
        if k in ['duedate', 'startdate', 'duetime', 'starttime']:
            task[k] = mktime(p.parse(task[k])[0])
        if k == 'priority': task[k] = len(task[k])
    return task

def parse(task, lex=None):
    if not lex:
        lex = build_lexer(join(CONFIGDIR, "lexer.pickle"))
    r = StringIO(task)
    scanner = Scanner(lex, r, "raw task")
    parsedtask = {}
    while 1:
        token = scanner.read()
        if token[0] == 'newline' or token[0] is None:
            if len(parsedtask.keys()) > 0:
                return rationalize(parsedtask)
        else:
            parsedtask[token[0]] = token[1]
