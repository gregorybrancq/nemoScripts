#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Convert bmp to jpg
"""

# Import
import logging

from common import createLog, parsingLine
from nemoBase import NemoBase


class ConvertBmp2Jpg(NemoBase):
    def __init__(self, root_log, args):
        root_log_name = '.'.join([root_log, self.__class__.__name__])
        self.logCB = logging.getLogger(root_log_name)
        auth_ext = [".tif", ".TIF", ".gif", ".GIF", ".bmp", ".BMP"]
        res_ext = ".jpg"
        msg_not_found = "No image has been found."
        super().__init__(root_log, root_log_name, args, auth_ext, res_ext, msg_not_found)


def main():
    # Create log class
    root_log = 'convertBmp2Jpg'
    (parsedArgs, args) = parsingLine()
    logger = createLog(root_log, parsedArgs)
    logger.info("START")
    ConvertBmp2Jpg(root_log, args).run()
    logger.info("STOP")


if __name__ == '__main__':
    main()
