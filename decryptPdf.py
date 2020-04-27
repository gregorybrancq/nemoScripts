#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Decrypt pdf file
'''



## Import
import sys
import os
from datetime import datetime
import subprocess
from optparse import OptionParser
from shutil import copyfile

## common
from python_common import *
HEADER = "DecryptPDF"

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
errC = 0

###############################################





###############################################
###############################################
##                FUNCTIONS                  ##
###############################################
###############################################

def decryptFile(fileList) :
    global log
    global errC
    log.info(HEADER, "In  decryptFile")

    for (fileD, fileN, fileE) in fileList :

        cmd='qpdf --decrypt "' + os.path.join(fileD, fileN + fileE) + '" "' + os.path.join(fileD, fileN + fileE) + '_tmp"'
        print("cmd=" + cmd)
        log.info(HEADER, "In  decryptFile cmd=" + str(cmd))
        procPopen = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT)
        procPopen.wait()
        if (procPopen.returncode != 0) :
            errC += 1
            log.error(HEADER, "In  decryptFile file: issue with " + str(cmd))
        else :
            # copy result file
            copyfile(os.path.join(fileD, fileN + fileE + '_tmp'), os.path.join(fileD, fileN + fileE))
            # delete temporary file
            os.remove(os.path.join(fileD, fileN + fileE + '_tmp'))

    log.info(HEADER, "Out decryptFile")



def cleanFiles(fileList, firstN, outputN) :
    global log
    global errC
    log.info(HEADER, "In  cleanFiles")

    for (fileD, fileN, fileE) in fileList :
        if os.path.exists(os.path.join(fileD, fileN + fileE)):
            os.remove(os.path.join(fileD, fileN + fileE))

    if os.path.exists(outputN) :
        os.rename(outputN, firstN + ".pdf")

    log.info(HEADER, "Out cleanFiles")

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
    warnC = 0
    firstN = str()
    outputN = str()
    log.info(HEADER, "In  main")

    fileList = list()

    log.info(HEADER, "In  main parsedArgs=" + str(parsedArgs))
    log.info(HEADER, "In  main args=" + str(args))

    ## Create list of files
    extAuth=[".pdf", ".PDF"]
    (fileList, warnC) = listFromArgs(log, HEADER, args, extAuth)

    ## Verify if there is at least one file to convert
    if (len(fileList) == 0) :
        log.exit("Decrypt PDF file", "No PDF file has been found\n")

    ## Decrypt them
    log.dbg("fileListConvert="+str(fileList))
    decryptFile(fileList)

    ## End dialog
    MessageDialogEnd(warnC, errC, logFile, "Decrypt pdf file", "\nJob fini.")
    
    log.info(HEADER, "Out main")

###############################################




if __name__ == '__main__':
 
    ## Create log class
    log = LOGC(logFile, HEADER, parsedArgs.debug)

    main()

