#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Convert jpg to webp
"""

# Import
import logging

from common import createLog, parsingLine
from nemoBase import NemoBase


class ConvertJpg2Wepb(NemoBase):
    def __init__(self, root_log, args):
        root_log_name = '.'.join([root_log, self.__class__.__name__])
        self.logCB = logging.getLogger(root_log_name)
        super().__init__(root_log, root_log_name, args)

    def run(self, no_windows=False):
        command = "cwebp"
        command_options = "-q 90 -o"
        command_set_output = True
        delete_file = False
        auth_ext = [".jpg", ".jpeg", ".png"]
        res_ext = ".webp"
        msg_not_found = "No image has been found."
        self.setConfig(command, command_options, command_set_output, delete_file,
                       auth_ext, res_ext, msg_not_found)
        self.runCommand(no_windows)


def main():
    # Create log class
    root_log = 'convertJpg2Webp'
    (parsedArgs, args) = parsingLine()
    logger = createLog(root_log, parsedArgs)
    logger.info("START")
    ConvertJpg2Wepb(root_log, args).run()
    logger.info("STOP\n")


if __name__ == '__main__':
    main()
