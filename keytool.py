# Implementation of java keytool utility in jython

import sys

from java.io import *
from java.security import *
from java.security.cert import *

# Command options for the utility. The boolean indicates whether the
# command option needs an additional argument or not
COMMAND_OPTIONS = {
    #'list' : False,
    'storepass' : False,
    'keystore' : True,
    'storepass' : True,
    'storetype' : True,
    'provider' : True
}

COMMAND_FUNCTION_MAP = {
    'list' : 'list_keytool',
    'help' : 'usage'
}

# Options dictionary with default values set
options = {
    'storetype' : 'JKS'
}
 
verbose = False
command = None
keystore = None

def list_keytool():
    print "Keystore type: ", keystore.getType()
    print "Keystore provider: ", keystore.getProvider().getName()

    print "The keystore contains ", keystore.size(), " entries"

    for alias in keystore.aliases():
        print "Alias name: ", alias
        print "Creation date: ", keystore.getCreationDate(alias)

        entryType = ''
        if keystore.isCertificateEntry(alias): 
            entryType = 'Certificate'
        elif keystore.isKeyEntry(alias):
            entryType = 'Key'
        print "Entry Type: ", entryType

        if keystore.entryInstanceOf(alias, KeyStore.PrivateKeyEntry):
            certs = keystore.getCertificateChain(alias)
            print "Certificate chain length: ", len(certs)
            for cert in certs:
                print str(cert)

        print "*******************************************"

def usage():
    print '''
keytool usage:

-help

-list        [-v | -rfc] 
            [-alias <alias>]
            [-keystore <keystore>] [-storepass <storepass>]
            [-storetype <storetype>] [-provider <provider_name>]
        '''

def parseOptions(argv):
    if len(argv) == 0:
        usage()

    i = 0
    while i < len(argv):
        arg = argv[i]
        cmd = ''

        #print "i = ", i, " arg = ", arg

        if arg.startswith('-'):
            cmd = arg[1:]
            if cmd in COMMAND_FUNCTION_MAP.keys():
                global command
                command = cmd
                i = i + 1
                continue
            elif arg == '-v':
                verbose = True
            elif cmd not in COMMAND_OPTIONS.keys():
                print "Bad command: ", arg

        if cmd in COMMAND_OPTIONS.keys():
            if COMMAND_OPTIONS[cmd]:
                i = i + 1
                if i == len(argv):
                    print "Error: Not enough arguments for option ", cmd
                    sys.exit(1)
                
                options[cmd] = argv[i]
        else:
            print "Error: Unknown option", cmd
            usage()
            sys.exit(1)

        i = i + 1

def execute():
    global keystore

    # initialze the variables
    ks = FileInputStream(File(options['keystore']))
    if options.has_key('provider'):
        keystore = KeyStore.getInstance(options['storetype'], options['provider'])
    else:
        keystore = KeyStore.getInstance(options['storetype'])

    keystore.load(ks, options['storepass'])

    funcName = COMMAND_FUNCTION_MAP[command]
    exec funcName + "()"

def keytool(argv):
    parseOptions(argv)
    execute()

if __name__ == '__main__':
    keytool(sys.argv[1:])
