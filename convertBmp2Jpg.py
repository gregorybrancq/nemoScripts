#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Convert bmp to jpg
"""

# Import
import logging

from log import createLog
from nemoBase import NemoBase


class ConvertBmp2Jpg(NemoBase):
    def __init__(self, root_log):
        root_log_name = '.'.join([root_log, self.__class__.__name__])
        self.logCB = logging.getLogger(root_log_name)
        auth_ext = [".tif", ".TIF", ".gif", ".GIF", ".bmp", ".BMP"]
        res_ext = ".jpg"
        super().__init__(root_log_name, auth_ext, res_ext)


def main():
    # Create log class
    root_log = 'convertBmp2Jpg'
    logger = createLog(root_log)
    ConvertBmp2Jpg(root_log).run()


if __name__ == '__main__':
    main()
