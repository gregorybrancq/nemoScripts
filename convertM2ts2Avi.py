#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Convert m2ts to avi
"""

# Import
import logging

from common import createLog, parsingLine
from nemoBase import NemoBase


class ConvertM2ts2Avi(NemoBase):
    def __init__(self, root_log, args):
        root_log_name = '.'.join([root_log, self.__class__.__name__])
        self.logCB = logging.getLogger(root_log_name)
        super().__init__(root_log, root_log_name, args)

    def run(self):
        command = "ffmpeg -threads 3 -r 29.97 -vcodec libxvid -s 1024x576 \
                  -aspect 16:9 -b 2000k -qmin 3 -qmax 5 -bufsize 4096 -mbd 2 \
                  -bf 2 -acodec libmp3lame -ar 48000 -ab 128k -ac 2 -i"
        command_options = ""
        command_set_output = True
        delete_file = True
        auth_ext = [".m2ts", ".M2TS"]
        res_ext = ".avi"
        msg_not_found = "No video has been found."
        self.setConfig(command, command_options, command_set_output, delete_file, auth_ext, res_ext, msg_not_found)
        self.runCommand()


def main():
    # Create log class
    root_log = 'convertM2ts2Avi'
    (parsedArgs, args) = parsingLine()
    logger = createLog(root_log, parsedArgs)
    logger.info("START")
    ConvertM2ts2Avi(root_log, args).run()
    logger.info("STOP")


if __name__ == '__main__':
    main()
