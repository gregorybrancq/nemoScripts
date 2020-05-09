#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Search & remove duplicate files thanks to fslint program
"""

# Import
import logging

from common import createLog, parsingLine
from nemoProgram import NemoProgram


class DuplicateFile(NemoProgram):
    def __init__(self, root_log, args):
        root_log_name = '.'.join([root_log, self.__class__.__name__])
        self.logCB = logging.getLogger(root_log_name)
        super().__init__(root_log, root_log_name, args)

    def run(self):
        command = "fslint-gui"
        self.setConfig(command)
        self.runCommand()


def main():
    # Create log class
    root_log = 'duplicateFile'
    (parsedArgs, args) = parsingLine()
    logger = createLog(root_log, parsedArgs)
    logger.info("START")
    DuplicateFile(root_log, args).run()
    logger.info("STOP\n")


if __name__ == '__main__':
    main()
