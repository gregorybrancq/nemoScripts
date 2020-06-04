#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Convert webm to mp4
"""

# Import
import logging

from common import createLog, parsingLine
from nemoBase import NemoBase


class ConvertWebm2Mp4(NemoBase):
    def __init__(self, root_log, args):
        root_log_name = '.'.join([root_log, self.__class__.__name__])
        self.logCB = logging.getLogger(root_log_name)
        super().__init__(root_log, root_log_name, args)

    def run(self, no_windows=False):
        command = "ffmpeg -i"
        command_options = ""
        command_set_output = True
        delete_file = True
        auth_ext = [".webm"]
        res_ext = ".mp4"
        msg_not_found = "No video has been found."
        self.setConfig(command, command_options, command_set_output, delete_file,
                       auth_ext, res_ext, msg_not_found)
        self.runCommand(no_windows)


def main():
    # Create log class
    root_log = 'convertWebm2Mp4'
    (parsedArgs, args) = parsingLine()
    logger = createLog(root_log, parsedArgs)
    logger.info("START")
    ConvertWebm2Mp4(root_log, args).run()
    logger.info("STOP\n")


if __name__ == '__main__':
    main()
