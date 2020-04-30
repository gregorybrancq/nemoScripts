#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Rotate images depending on the EXIF information
"""

# Import
import logging

from common import createLog, parsingLine
from nemoBase import NemoBase


class ConvertExif(NemoBase):
    def __init__(self, root_log, args):
        root_log_name = '.'.join([root_log, self.__class__.__name__])
        self.logCB = logging.getLogger(root_log_name)
        super().__init__(root_log, root_log_name, args)

    def run(self):
        command = "exifautotran"
        command_param = False
        delete_file = False
        auth_ext = [".JPG", ".jpg", ".JPEG", ".jpeg"]
        res_ext = ""
        msg_not_found = "No image has been found."
        self.setConfig(command, command_param, delete_file, auth_ext, res_ext, msg_not_found)
        self.runCommand()


def main():
    # Create log class
    root_log = 'exifConvert'
    (parsedArgs, args) = parsingLine()
    logger = createLog(root_log, parsedArgs)
    logger.info("START")
    ConvertExif(root_log, args).run()
    logger.info("STOP")


if __name__ == '__main__':
    main()
