#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Decrypt pdf file
"""

# Import
import logging
from shutil import copyfile

from common import createLog, parsingLine
from nemoBase import NemoBase


class DecryptPdf(NemoBase):
    def __init__(self, root_log, args):
        root_log_name = '.'.join([root_log, self.__class__.__name__])
        self.logCB = logging.getLogger(root_log_name)
        super().__init__(root_log, root_log_name, args)

    def replace(self, file_name):
        self.logCB.debug("Copy result file")
        copyfile(self.temp_file, file_name + self.res_ext)

    def run(self):
        command = "qpdf --decrypt"
        command_options = ""
        command_set_output = True
        delete_file = False
        auth_ext = [".pdf", ".PDF"]
        res_ext = ".pdf"
        msg_not_found = "No pdf file has been found."
        self.setConfig(command, command_options, command_set_output,
                       delete_file, auth_ext, res_ext, msg_not_found)
        self.runCommand()


def main():
    # Create log class
    root_log = 'decryptPdf'
    (parsedArgs, args) = parsingLine()
    logger = createLog(root_log, parsedArgs)
    logger.info("START")
    DecryptPdf(root_log, args).run()
    logger.info("STOP")


if __name__ == '__main__':
    main()
