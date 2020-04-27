#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Convert bmp to jpg
"""

# Import
import os
import logging
import subprocess
from optparse import OptionParser

from log import createLog
from nemoBase import NemoBase
#sys.path.append('/home/greg/Greg/work/env/pythonCommon')
#from message import MessageDialogEnd
#from basic import getLogDir

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

count_error = 0

class ConvertBmp2Jpg(NemoBase):
    def __init__(self, root_log):
        root_log_name = '.'.join([root_log, self.__class__.__name__])
        self.logCB = logging.getLogger(root_log_name)
        auth_ext = [".tif", ".TIF", ".gif", ".GIF", ".bmp", ".BMP"]
        res_ext = ".jpg"
        arguments = args
        super().__init__(root_log_name, arguments, auth_ext, res_ext)


    ## End dialog
    #MessageDialogEnd(count_warn, count_error, logFile, "Convert images", "\nJob fini.")


##############################################
#                 MAIN
##############################################

def main():
    # Create log class
    root_log = 'convertBmp2Jpg'
    logger = createLog(root_log)
    ConvertBmp2Jpg(root_log).run()

##############################################


if __name__ == '__main__':
    main()
