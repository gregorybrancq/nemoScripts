#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Convert X pdf to 1 pdf
"""

# Import
import logging

from common import createLog, parsingLine
from nemoOneCommand import NemoOneCommand


class ConcatPdf(NemoOneCommand):
    def __init__(self, root_log, args):
        root_log_name = '.'.join([root_log, self.__class__.__name__])
        self.logCB = logging.getLogger(root_log_name)
        super().__init__(root_log, root_log_name, args)

    def run(self):
        command = "pdftk"
        file_list_option = ""
        command_output_option = "cat output"
        delete_file = True
        auth_ext = [".pdf", ".PDF"]
        msg_not_found = "No pdf file has been found."
        res_file = ""
        self.setConfig(command, file_list_option, command_output_option,
                       delete_file, auth_ext, res_file, msg_not_found)
        self.runCommand()


def main():
    # Create log class
    root_log = 'concatXPdf21Pdf'
    (parsedArgs, args) = parsingLine()
    logger = createLog(root_log, parsedArgs)
    logger.info("START")
    ConcatPdf(root_log, args).run()
    logger.info("STOP\n")


if __name__ == '__main__':
    main()
