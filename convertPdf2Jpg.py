#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Convert pdf to jpg
"""

# Import
import logging

from common import createLog, parsingLine
from nemoBase import NemoBase


class ConvertPdf2Jpg(NemoBase):
    def __init__(self, root_log, args):
        root_log_name = '.'.join([root_log, self.__class__.__name__])
        self.logCB = logging.getLogger(root_log_name)
        super().__init__(root_log, root_log_name, args)

    def run(self):
        command = "convert -density 248x248"
        command_param = True
        auth_ext = [".pdf", ".PDF"]
        res_ext = ".jpg"
        msg_not_found = "No image has been found."
        self.setConfig(command, command_param, auth_ext, res_ext, msg_not_found)
        self.runOneCommand()


def main():
    # Create log class
    root_log = 'convertPdf2Jpg'
    (parsedArgs, args) = parsingLine()
    logger = createLog(root_log, parsedArgs)
    logger.info("START")
    ConvertPdf2Jpg(root_log, args).run()
    logger.info("STOP")


if __name__ == '__main__':
    main()
