#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Reduce the image size
"""

# Import
import sys
import logging

from common import createLog, parsingLine
from nemoBase import NemoBase

sys.path.append('/home/greg/Greg/work/env/pythonCommon')
from message import MessageDialog


class PhotoReduce(NemoBase):
    def __init__(self, root_log, args):
        root_log_name = '.'.join([root_log, self.__class__.__name__])
        self.logCB = logging.getLogger(root_log_name)
        super().__init__(root_log, root_log_name, args)

    def askPercent(self):
        win_title = "Reduce photo size"
        resize_percent_str = MessageDialog(dialog_type='entry', title=win_title,
                                           message1="Quelle est le pourcentage de réduction ?").run()
        try :
            resize_percent=int(resize_percent_str)
        except ValueError :
            MessageDialog(type_='error', title=win_title,
                          message="\nle pourcentage doit être un chiffre entre 0 et 100.\n").run()
            sys.exit(1)
        self.logCB.debug("resize_percent=%s"%str(resize_percent))
        return resize_percent

    def run(self):
        resize_percent = self.askPercent()
        command='mogrify -resize ' + str(resize_percent) + '%'
        command_options = ""
        command_set_output = False
        delete_file = False
        auth_ext = [".jpg", ".jpeg", ".tif", ".gif", ".bmp"]
        res_ext = ""
        msg_not_found = "No image has been found."
        self.setConfig(command, command_options, command_set_output,
                       delete_file, auth_ext, res_ext, msg_not_found)
        self.runCommand()


def main():
    # Create log class
    root_log = 'photoReduce'
    (parsedArgs, args) = parsingLine()
    logger = createLog(root_log, parsedArgs)
    logger.info("START")
    PhotoReduce(root_log, args).run()
    logger.info("STOP\n")


if __name__ == '__main__':
    main()
