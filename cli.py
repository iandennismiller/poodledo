#!/usr/bin/python

from ConfigParser import SafeConfigParser,NoOptionError,NoSectionError
from apiclient import ApiClient,ToodledoError
from getpass import getpass
from os import mkdir
from os.path import exists, expanduser, join

CONFIGDIR  = expanduser("~/.tdcli")
CONFIGFILE = join(CONFIGDIR, "tdclirc")

def get_config():
    config = SafeConfigParser()
    config.read(CONFIGFILE)
    return config

def store_config(config):
    if not exists(CONFIGDIR):
        mkdir(CONFIGDIR)
    cfile = open(CONFIGFILE, 'w')
    config.write(cfile)
    cfile.close()

def read_or_get_creds(config):
    username = ""
    password = ""

    try:
        username = config.get('config', 'username')
        password = config.get('config', 'password')
    except (NoOptionError, NoSectionError):
        print "Please enter your login credentials."
        username = raw_input("Username: ")
        password = getpass("Password: ")

    return (username, password)

def do_login(config=None):
    client = ApiClient()
    if not config:
        config = get_config()
    try:
        client._key = config.get('session', 'key')
        client.getAccountInfo()

    except (NoSectionError, NoOptionError, ToodledoError):
        # cached session key either wasn't there or wasn't good; get a new one and cache it
        client._key = None
        (username, password) = read_or_get_creds(config)

        try:
            client.authenticate(username, password)
        except ToodledoError as e:
            print "No login credentials were successful; please try again."
            raise e

        if not config.has_section('session'):
            config.add_section('session')
        config.set('session', 'key', client.key)
        store_config(config)

    return client
