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
    def __init__(self, root_log, args, delete_file=True):
        root_log_name = '.'.join([root_log, self.__class__.__name__])
        self.logCB = logging.getLogger(root_log_name)
        self.delete_file = delete_file
        super().__init__(root_log, root_log_name, args)

    def run(self, no_windows=False):
        command = "convert"
        command_options = ""
        command_set_output = True
        auth_ext = [".tif", ".gif", ".bmp"]
        res_ext = ".jpg"
        msg_not_found = "No image has been found."
        self.setConfig(command, command_options, command_set_output,
                       self.delete_file, auth_ext, res_ext, msg_not_found)
        self.runCommand(no_windows)


def main():
    # Create log class
    root_log = 'convertBmp2Jpg'
    (parsedArgs, args) = parsingLine()
    logger = createLog(root_log, parsedArgs)
    logger.info("START")
    ConvertBmp2Jpg(root_log, args).run()
    logger.info("STOP\n")


if __name__ == '__main__':
    main()
