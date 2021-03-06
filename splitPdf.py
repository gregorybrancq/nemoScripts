#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Split 1 pdf to X pdf
"""

# Import
import logging
import os
import subprocess

import send2trash

from common import createLog, parsingLine
from nemoBase import NemoBase


class SplitPdf(NemoBase):
    def __init__(self, root_log, args):
        root_log_name = '.'.join([root_log, self.__class__.__name__])
        self.logCB = logging.getLogger(root_log_name)
        super().__init__(root_log, root_log_name, args)

    def run(self):
        command = "pdftk"
        command_options = "burst output"
        command_set_output = True
        delete_file = False
        auth_ext = [".pdf"]
        res_ext = "_%04d.pdf"
        msg_not_found = "No pdf file has been found."
        self.setConfig(command, command_options, command_set_output,
                       delete_file, auth_ext, res_ext, msg_not_found)
        self.runCommand()


def main():
    # Create log class
    root_log = 'splitPdf'
    (parsedArgs, args) = parsingLine()
    logger = createLog(root_log, parsedArgs)
    logger.info("START")
    SplitPdf(root_log, args).run()
    logger.info("STOP\n")


if __name__ == '__main__':
    main()
