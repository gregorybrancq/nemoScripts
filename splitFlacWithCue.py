#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Split flac file into several ones thanks to cue file
"""

# Import
import logging
import os
import subprocess
import sys

from common import createLog, parsingLine
from message import MessageDialogEnd
from nemoBase import NemoBase


class SplitFlacWithCue(NemoBase):
    def __init__(self, root_log, args):
        root_log_name = '.'.join([root_log, self.__class__.__name__])
        self.logSFC = logging.getLogger(root_log_name)
        super().__init__(root_log, root_log_name, args)

    def warningInputFiles(self):
        MessageDialogEnd(error=True, log_file=self.log_name, title=self.prog_name,
                         msg1="ERROR", msg2=self.msg_not_found)
        self.logSFC.error(self.msg_not_found)
        sys.exit(1)

    def compute(self):
        file_flac = ""
        dir_flac = ""
        file_cue = ""
        dir_cue = ""
        for (dir_name, file_name, file_ext) in self.file_list_in:
            self.logSFC.debug("dir = %s, file = %s, ext = %s" % (dir_name, file_name, file_ext))
            if dir_name != "":
                os.chdir(dir_name)

            if file_ext == ".flac":
                file_flac = file_name + file_ext
                dir_flac = dir_name
            elif file_ext == ".cue":
                file_cue = file_name + file_ext
                dir_cue = dir_name

        if (not file_flac or not file_cue) and dir_cue != dir_flac:
            self.warningInputFiles()

        # Construct the command
        if dir_flac:
            os.chdir(dir_flac)
        self.command = 'shntool split'
        cmd = self.command.split(" ")
        cmd.append('-t')
        cmd.append('%p - %a - %n - %t')
        cmd.append("-f")
        cmd.append(file_cue)
        cmd.append("-o")
        cmd.append("flac")
        cmd.append(file_flac)

        self.logNB.info("Run command %s" % str(cmd))

        # Execute the command
        process = subprocess.Popen(cmd, stderr=subprocess.STDOUT)
        process.wait()
        if process.returncode != 0:
            self.error = True
            self.msg_end += "In %s, cmd failed : \n  %s\n" % (os.getcwd(), str(cmd))
        else:
            self.msg_end += "Executed :\n  %s\n  %s\n" % (file_flac, file_cue)

    def run(self):
        command = "shntool"
        command_options = ""
        command_set_output = False
        delete_file = False
        auth_ext = [".flac", ".FLAC", ".cue", ".CUE"]
        res_ext = ""
        msg_not_found = "Need exactly 2 audio files in same directory : .flac and .cue."
        self.setConfig(command, command_options, command_set_output, delete_file,
                       auth_ext, res_ext, msg_not_found)

        self.getFileList()
        if len(self.file_list_in) != 2:
            self.warningInputFiles()
        else:
            self.compute()
        self.analyze()


def main():
    # Create log class
    root_log = 'splitFlac'
    (parsedArgs, args) = parsingLine()
    logger = createLog(root_log, parsedArgs)
    logger.info("START")
    SplitFlacWithCue(root_log, args).run()
    logger.info("STOP")


if __name__ == '__main__':
    main()
