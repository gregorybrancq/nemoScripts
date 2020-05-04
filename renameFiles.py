#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Rename files in the same directory
"""

# Import
import logging

from common import createLog, parsingLine
from nemoBase import NemoBase


class RenameFiles(NemoBase):
    def __init__(self, root_log, args):
        root_log_name = '.'.join([root_log, self.__class__.__name__])
        self.logCB = logging.getLogger(root_log_name)
        super().__init__(root_log, root_log_name, args)

    def run(self):
        command = "pyrenamer"
        command_options = ""
        command_set_output = False
        delete_file = False
        auth_ext = []
        res_ext = ""
        msg_not_found = "No file has been found."
        self.setConfig(command, command_options, command_set_output, delete_file, auth_ext, res_ext, msg_not_found)
        self.runProgram()


def main():
    # Create log class
    root_log = 'renameFiles'
    (parsedArgs, args) = parsingLine()
    logger = createLog(root_log, parsedArgs)
    logger.info("START")
    RenameFiles(root_log, args).run()
    logger.info("STOP")


if __name__ == '__main__':
    main()
