#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Convert bmp to jpg
"""

# Import
import logging
import sys
import os
from datetime import datetime
import subprocess
from optparse import OptionParser

from log2 import createLog
from nemoBase import NemoBase
#sys.path.append('/home/greg/Greg/work/env/pythonCommon')
#from message import MessageDialogEnd
#from basic import getLogDir, listFromArgs
#from log import LOGC

HEADER = "BmpTOJpg"

# directory
#logDir = getLogDir()

##############################################


##############################################
#              Line Parsing
##############################################

parser = OptionParser()

parser.add_option(
    "-d",
    "--debug",
    action="store_true",
    dest="debug",
    default=False,
    help="Display all debug information"
)

(parsedArgs, args) = parser.parse_args()

###############################################


##############################################
# Global variables
##############################################

t = str(datetime.today().isoformat("_"))
#logFile = os.path.join(logDir, HEADER + "_" + t + ".log")
count_error = 0

##############################################

##############################################
#                FUNCTIONS
##############################################

def convertFile(file_list):
    global log
    global count_error
    log.info(HEADER, "In  convertFile")

    old_dir = os.getcwd()

    for (dir_name, file_name, file_ext) in file_list:
        log.info(HEADER, "In  convertFile directory " + str(dir_name) + "  convertFile " + file_name + file_ext)

        if dir_name != "":
            os.chdir(dir_name)

        cmd = 'convert "' + file_name + file_ext + '" "' + file_name + '.jpg"'
        log.info(HEADER, "In  convertFile cmd=" + str(cmd))
        proc = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT)
        proc.wait()
        if proc.returncode != 0:
            count_error += 1
            log.error(HEADER, "In  convertFile file: issue with " + str(os.path.join(dir_name, file_name + file_ext)))

        if dir_name != "":
            os.chdir(old_dir)

    log.info(HEADER, "Out convertFile")

##############################################


class ConvertBmp2Jpg(NemoBase):
    def __init__(self, root_log):
        super().__init__('.'.join([root_log, self.__class__.__name__]))
        self.logger = logging.getLogger('.'.join([root_log, self.__class__.__name__]))
        self.nom="Toto"
        self.logger.info("Info in init in ConvertBmp2Jpg")

    def pp(self):
        print(self.nom)
        self.logger.info("Info from pp in ConvertBmp2Jpg")


##############################################
#                 MAIN
##############################################

def main():
    # Create log class
    root_log = 'Bmp2Jpg'
    logger = createLog(root_log)
    logger.info("first comment in main convertBmp2Jpg")
    convertBmp2Jpg = ConvertBmp2Jpg(root_log)
    #convertBmp2Jpg.logger_one.info("info from convertBmp2Jpg main")
    logger.info("Info in main with logger")
    convertBmp2Jpg.pp()
    convertBmp2Jpg.oo()
    print("Out Main")

    #global log
    #count_warn = 0
    #log.info(HEADER, "In  main")

    #log.info(HEADER, "In  main parsedArgs=" + str(parsedArgs))
    #log.info(HEADER, "In  main args=" + str(args))

    ## Create list of files
    #auth_ext = [".tif", ".TIF", ".gif", ".GIF", ".bmp", ".BMP"]
    #(file_list, count_warn) = listFromArgs(log, HEADER, args, auth_ext)

    ## Verify if there is at least one file to convert
    #if len(file_list) == 0:
    #    log.exit("Convert BMP to JPG", "No image has been found\n")

    ## Convert them
    #log.dbg("file_list=" + str(file_list))
    #convertFile(file_list)

    ## End dialog
    #MessageDialogEnd(count_warn, count_error, logFile, "Convert images", "\nJob fini.")

    #log.info(HEADER, "Out main")

##############################################


if __name__ == '__main__':
    #log = LOGC(logFile, HEADER, parsedArgs.debug)

    main()
