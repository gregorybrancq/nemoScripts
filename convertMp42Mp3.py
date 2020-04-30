#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Convert MP4 to MP3
"""

# Import
import logging

from common import createLog, parsingLine
from nemoBase import NemoBase


class ConvertMp42Mp3(NemoBase):
    def __init__(self, root_log, args):
        root_log_name = '.'.join([root_log, self.__class__.__name__])
        self.logCB = logging.getLogger(root_log_name)
        super().__init__(root_log, root_log_name, args)

    def run(self):
        command = 'pacpl --to mp3 -bitrate 320'
        command_param = False
        delete_file = False
        auth_ext = [".mp4", ".MP4"]
        res_ext = ".mp3"
        msg_not_found = "No video has been found."
        self.setConfig(command, command_param, delete_file, auth_ext, res_ext, msg_not_found)
        self.runOneCommand()



def main():
    # Create log class
    root_log = 'convertMp42Mp3'
    (parsedArgs, args) = parsingLine()
    logger = createLog(root_log, parsedArgs)
    logger.info("START")
    ConvertMp42Mp3(root_log, args).run()
    logger.info("STOP")


if __name__ == '__main__':
    main()
