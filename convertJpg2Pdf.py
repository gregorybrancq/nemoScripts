#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Convert jpg to pdf
"""

# Import
import logging

from common import createLog, parsingLine
from nemoBase import NemoBase


class ConvertJpg2Pdf(NemoBase):
    def __init__(self, root_log, args):
        root_log_name = '.'.join([root_log, self.__class__.__name__])
        self.logCB = logging.getLogger(root_log_name)
        super().__init__(root_log, root_log_name, args)

    def run(self, no_windows=False):
        command = "convert"
        command_options = ""
        command_set_output = True
        delete_file = True
        auth_ext = [".jpg", ".JPG", ".jpeg", ".JPEG", ".tif", ".TIF",
                    ".gif", ".GIF", ".bmp", ".BMP"]
        res_ext = ".pdf"
        msg_not_found = "No image has been found."
        self.setConfig(command, command_options, command_set_output,
                       delete_file, auth_ext, res_ext, msg_not_found)
        self.runCommand(no_windows)


def main():
    # Create log class
    root_log = 'convertJpg2Pdf'
    (parsedArgs, args) = parsingLine()
    logger = createLog(root_log, parsedArgs)
    logger.info("START")
    logger.debug("args = %s"%str(args))
    ConvertJpg2Pdf(root_log, args).run()
    logger.info("STOP")


if __name__ == '__main__':
    main()
