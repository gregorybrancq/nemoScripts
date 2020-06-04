#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Reduce the weight of the pdf files
"""

# Import
import logging
import os
import shutil
import sys

sys.path.append('/home/greg/Greg/work/env/pythonCommon')
from basic import humanSize
from common import createLog, parsingLine
from nemoBase import NemoBase


class ReducePdfWeight(NemoBase):
    def __init__(self, root_log, args):
        root_log_name = '.'.join([root_log, self.__class__.__name__])
        self.logCB = logging.getLogger(root_log_name)
        super().__init__(root_log, root_log_name, args)

    def replace(self, file_name):
        # is it worth to move the result?
        original_size = os.path.getsize(file_name)
        reduced_size = os.path.getsize(self.temp_file)
        self.logCB.debug("Original file (%s) = %s\tReduced file (%s) = %s" %
                         (file_name, humanSize(original_size),
                          self.temp_file, humanSize(reduced_size)))

        if original_size - reduced_size > 0 :
            self.msg_end += "Reduced file : %s\n" % (os.path.join(os.getcwd(), file_name))
            # move file
            if os.path.exists(file_name):
                os.remove(file_name)
            shutil.move(self.temp_file, file_name)
        else :
            self.msg_end += "Keep original file : %s\n" % (os.path.join(os.getcwd(), file_name))
            self.logCB.debug("Delete reduced file")
            # remove result file
            if os.path.exists(self.temp_file):
                os.remove(self.temp_file)

    def run(self):
        command = "gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=output_file_to_replace"
        command_options = ""
        command_set_output = True
        delete_file = False
        auth_ext = [".pdf"]
        res_ext = ".pdf"
        msg_not_found = "No pdf file has been found."
        self.setConfig(command, command_options, command_set_output, delete_file,
                       auth_ext, res_ext, msg_not_found)
        self.runCommand()


def main():
    # Create log class
    root_log = 'reducePdfWeight'
    (parsedArgs, args) = parsingLine()
    logger = createLog(root_log, parsedArgs)
    logger.info("START")
    ReducePdfWeight(root_log, args).run()
    logger.info("STOP\n")


if __name__ == '__main__':
    main()
