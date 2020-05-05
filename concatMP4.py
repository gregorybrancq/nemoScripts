#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Convert X mp4 to 1 mp4
"""

# Import
import logging

from common import createLog, parsingLine
from nemoOneCommand import NemoOneCommand


class ConcatMP4(NemoOneCommand):
    def __init__(self, root_log, args):
        root_log_name = '.'.join([root_log, self.__class__.__name__])
        self.logCB = logging.getLogger(root_log_name)
        super().__init__(root_log, root_log_name, args)

    def run(self):
        command = "MP4Box"
        file_list_option = "-cat"
        command_output_option = "-new"
        delete_file = False
        auth_ext = [".mp4", ".MP4", ".avi", ".AVI"]
        msg_not_found = "No video has been found."
        res_file = ""
        self.setConfig(command, file_list_option, command_output_option,
                       delete_file, auth_ext, res_file, msg_not_found)
        self.runCommand()


def main():
    # Create log class
    root_log = 'concatXMp4to1Mp4'
    (parsedArgs, args) = parsingLine()
    logger = createLog(root_log, parsedArgs)
    logger.info("START")
    ConcatMP4(root_log, args).run()
    logger.info("STOP")


if __name__ == '__main__':
    main()
