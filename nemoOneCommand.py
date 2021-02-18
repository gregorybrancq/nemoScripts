#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Launch one command for selected files.
"""
import logging
import os
import subprocess
import sys

from nemoBase import NemoBase

sys.path.append('/home/greg/Tools/env/pythonCommon')


class NemoOneCommand(NemoBase):
    """Class NemoBase

    Specify some usual functions, and by default will execute the following computation runJob.
    """

    def __init__(self, log_name, root_log, arguments):
        """Initialization of the class

        :param log_name: it indicates the log name
        :param root_log: allows to keep hierarchy for logging
        :param arguments: arguments pass out to the file program (Nemo or Nautilus
        """
        root_log_name = '.'.join([root_log, __name__])
        self.logOC = logging.getLogger(root_log_name)
        self.logOC.debug("In init nemoOneCommand")
        super().__init__(log_name, root_log_name, arguments)
        self.file_list_option = str
        self.command_output_option = str
        self.res_file = str

    def setConfig(self, command, file_list_option, command_output_option,
                  delete_file, auth_ext, res_file, msg_not_found):
        """Set the configuration of the class parameters

        :param command: the command to execute
        :param file_list_option: options to set to each file in file_list
        :param command_output_option: specify the option before output file
        :param delete_file: delete the input file (default False)
        :param auth_ext: the authorized extension
        :param res_file: the output file name
        :param msg_not_found: if no file matches, it will indicate this message information
        :return: updated attributes
        """
        self.command = command
        self.file_list_option = file_list_option
        self.command_output_option = command_output_option
        self.delete_file = delete_file
        self.auth_ext = auth_ext
        self.res_file = res_file
        self.msg_not_found = msg_not_found

    def compute(self):
        """Execute the command for file_list.
        """
        # Initialize the command
        cmd = self.command.split(" ")
        output_file_name = ""
        output_file_ext = ""

        for (dir_name, file_name, file_ext) in self.file_list_in:
            # option for each file
            if self.file_list_option:
                in_opt = self.file_list_option.split(" ")
                cmd += in_opt

            # keep first file name for output file
            if output_file_name == "":
                output_file_name = file_name
                output_file_ext = file_ext

            # input file name
            cmd.append(os.path.join(dir_name, file_name + file_ext))

        # out option
        if self.command_output_option:
            out_opt = self.command_output_option.split(" ")
            cmd += out_opt

        # output name
        if not self.res_file:
            # no res_file given in parameter
            # need to define it
            find_name = False
            i = 0
            output_name = output_file_name + output_file_ext
            while not find_name:
                if not os.path.exists(output_name):
                    find_name = True
                else:
                    output_name = output_file_name + "_" + str(i) + output_file_ext
                    i += 1
            self.res_file = output_name
        cmd.append(self.res_file)

        self.logOC.debug("command = %s" % str(cmd))

        # Execute the command
        process = subprocess.Popen(cmd, stderr=subprocess.STDOUT)
        process.wait()
        if process.returncode != 0:
            # be sure that result file is not well generated (if expected)
            if not os.path.isfile(self.res_file):
                self.error = True
                self.msg_end += "cmd failed :\n  %s\n" % str(cmd)
        else:
            self.msg_end += "Executed : %s\n" % (os.path.join(os.getcwd(), self.res_file))
