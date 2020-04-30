#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Convert bmp to jpg
"""

# Import
import logging

from common import createLog, parsingLine
from nemoBase import NemoBase


class ConvertBmp2Jpg(NemoBase):
    def __init__(self, root_log, args):
        root_log_name = '.'.join([root_log, self.__class__.__name__])
        self.logCB = logging.getLogger(root_log_name)
        super().__init__(root_log, root_log_name, args)

    def run(self):
        command = "convert"
        command_param = True
        delete_file = True
        auth_ext = [".tif", ".TIF", ".gif", ".GIF", ".bmp", ".BMP"]
        res_ext = ".jpg"
        msg_not_found = "No image has been found."
        self.setConfig(command, command_param, delete_file, auth_ext, res_ext, msg_not_found)
        self.runOneCommand()


def main():
    # Create log class
    root_log = 'convertBmp2Jpg'
    (parsedArgs, args) = parsingLine()
    logger = createLog(root_log, parsedArgs)
    logger.info("START")
    ConvertBmp2Jpg(root_log, args).run()
    logger.info("STOP")


if __name__ == '__main__':
    main()
#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Send file(s) to DL FREE from nemo
'''



## Import
import sys
import os
import re
from datetime import datetime
from subprocess import Popen, PIPE
from optparse import OptionParser

## common
from python_common import *
HEADER = "FTP_FREE"

## directory
logDir   = getLogDir()

###############################################



###############################################
###############################################
##              Line Parsing                 ##
###############################################
###############################################

parsedArgs = {}
parser = OptionParser()


parser.add_option(
    "-d",
    "--debug",
    action  = "store_true",
    dest    = "debug",
    default = False,
    help    = "Display all debug information"
    )

(parsedArgs , args) = parser.parse_args()

###############################################



###############################################
## Global variables
###############################################

t = str(datetime.today().isoformat("_"))
logFile = os.path.join(logDir, HEADER + "_" + t + ".log")

###############################################





###############################################
###############################################
###############################################
##                 MAIN                      ##
###############################################
###############################################
###############################################


def main() :
    global log
    log.info(HEADER, "In  main")

    log.info(HEADER, "In  main parsedArgs=" + str(parsedArgs))
    log.info(HEADER, "In  main args=" + str(args))

    if args.__len__() != 1 :
        MessageDialog(type_='error', title="Send File to DL Free", message="Only 1 file supported").run()
        sys.exit(-1)

    fileN = ""
    if (os.path.isfile(args[0])) :
        fileN = args[0]
    else :
        MessageDialog(type_='error', title="Send File to DL Free", message=args[0] + " is not a file").run()
        sys.exit(-1)

    ## Launch the ftp free program
    out = ""
    err = ""
    cmdToLaunch='/home/greg/Greg/work/env/shellScripts/ftp-free.sh "' + str(fileN) + '"'
    log.info(HEADER, "In  main cmdToLaunch=" + str(cmdToLaunch))
    procPopen = Popen(cmdToLaunch, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = procPopen.communicate()
    log.info(HEADER, "In  main result out\n" + str(out))
    log.info(HEADER, "In  main result err\n" + str(err))

    ## Print result
    msg = "Fichier envoyé : " + str(fileN) + "\n\n"
    if re.search("Fichier d'origine :", out) :
        msg += "URL de download: " + "\n"
        msg += "    " + re.findall("URL Fichier depose : (.*)", out)[0] + "\n"
    if re.search("URL pour suppression du fichier :", out) :
        msg += "URL de suppression: " + "\n"
        msg += "    " + re.sub("&", "&amp;", re.findall("URL pour suppression du fichier : (.*)", out)[0]) + "\n"
    
    log.info(HEADER, "In  main msg = " + msg)
    log.info(HEADER, "In  main err = " + err)

    if (err != "") :
        MessageDialog(type_='error', title="Send File to DL Free", message=msg).run()
    else :
        MessageDialog(type_='info', title="Send File to DL Free", message=msg).run()

    ## Send email
    #log.info(HEADER, "In  main send mail")
    #log.info(HEADER, "In  main send mail args[0]=" + str(args[0]))
    #log.info(HEADER, "In  main send mail msg=" + str(msg))
    #try:
    #    sendMail("Greg <gregory.brancq@free.fr>", "gregory.brancq@free.fr", "", "Send to DL Free : " + str(args[0]), str(msg), "");
    #except :
    #    log.error(HEADER, "In  main send mail issue ")

    log.info(HEADER, "Out main")



if __name__ == '__main__':
 
    ## Create log class
    log = LOGC(logFile, HEADER, parsedArgs.debug)

    main()

###############################################

