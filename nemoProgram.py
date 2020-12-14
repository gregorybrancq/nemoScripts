#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Launch a program for selected directory.
"""
import logging
import os
import subprocess

from nemoBase import NemoBase


class NemoProgram(NemoBase):
    """Class NemoProgram

    To execute a program in the specified directory
    """

    def __init__(self, log_name, root_log, arguments):
        """Initialization of the class

        :param log_name: it indicates the log name
        :param root_log: allows to keep hierarchy for logging
        :param arguments: arguments pass out to the file program (Nemo or Nautilus
        """
        root_log_name = '.'.join([root_log, __name__])
        self.logNP = logging.getLogger(root_log_name)
        self.logNP.debug("In init nemoProgram")
        super().__init__(log_name, root_log_name, arguments)

    def setConfig(self, command):
        """Set the configuration of the class parameters

        :param command: the command to execute
        :return: updated attributes
        """
        self.command = command

    def compute(self):
        """Execute the program for the first argument.
        """
        (dir_name, file_name, file_ext) = self.file_list_in[0]
        cmd = self.command.split(" ")
        if dir_name != "":
            os.chdir(dir_name)
        cmd.append(os.getcwd())
        self.logNP.info("Run command : %s" % str(cmd))
        process = subprocess.Popen(cmd, stderr=subprocess.STDOUT)
        process.wait()

    def runCommand(self):
        """ Get the file list, execute the program only for the first argument.
        """
        self.getFileList()
        if len(self.file_list_in) != 0:
            self.compute()
