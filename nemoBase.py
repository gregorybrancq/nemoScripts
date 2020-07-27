#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Basic functions for file programs as Nemo or Nautilus.
"""
import logging
import os
import re
import subprocess
import sys

import send2trash

sys.path.append('/home/greg/Greg/work/env/pythonCommon')
from basic import getLogDir
from message import MessageDialogEnd


class NemoBase:
    """Class NemoBase

    Specify some usual functions, and by default will execute the following computation runJob.
    """

    def __init__(self, log_name, root_log, arguments):
        """Initialization of the class

        :param log_name: it indicates the log name
        :param root_log: allows to keep hierarchy for logging
        :param arguments: arguments pass out to the file program Nemo or Nautilus
        """
        self.logNB = logging.getLogger('.'.join([root_log, __name__]))
        self.logNB.debug("In init nemoBase")
        self.prog_name = log_name
        self.log_name = os.path.join(getLogDir(), log_name) + ".log"
        if type(arguments) != list:
            self.logNB.error("Arguments is not a list")
            sys.exit(1)
        self.arguments = arguments
        self.command = str()
        self.command_options = str()
        self.command_set_output = True
        self.delete_file = False
        self.auth_ext = list()
        self.res_ext = str()
        self.msg_not_found = str()
        self.file_list_in = list()
        self.file_list_out = list()
        self.msg_end = ""
        self.error = False
        self.temp_file = ""  # temporary file

    def setConfig(self, command, command_options, command_set_output, delete_file, auth_ext, res_ext, msg_not_found):
        """Set the configuration of the class parameters

        :param command: the command to execute
        :param command_options: options to set to the command after the file input
        :param command_set_output: specify the output file with extension to the command (default False)
        :param delete_file: delete the input file (default False)
        :param auth_ext: the authorized extension
        :param res_ext: the file extension result
        :param msg_not_found: if no file matches, it will indicate this message information
        :return: updated attributes
        """
        self.command = command
        self.command_options = command_options
        self.command_set_output = command_set_output
        self.delete_file = delete_file
        self.auth_ext = auth_ext
        self.res_ext = res_ext
        self.msg_not_found = msg_not_found

    def _addFile(self, file_name):
        """Function to be used internally with getFileList
        it checks if the selected file corresponds to the authorization extension
        and transforms the () characters

        :param file_name: the file to treat
        :return: update file_list attribute
        """
        self.logNB.debug("In  _addFile file_name=" + str(file_name))
        dir_n = os.path.dirname(file_name)
        dir_n1 = dir_n.replace('(', '\(')
        dir_n2 = dir_n1.replace(')', '\)')
        file_name_wo_dir = re.sub(dir_n2 + "\/", '', file_name)
        (fileN, extN) = os.path.splitext(file_name_wo_dir)
        if len(self.auth_ext) == 0 or self.auth_ext.__contains__(extN) \
                or self.auth_ext.__contains__(extN.lower()) \
                or self.auth_ext.__contains__(extN.upper()):
            self.logNB.debug("In  _addFile dir_n=" + str(dir_n) + ", fileN=" + str(fileN) + ", extN=" + str(extN))
            self.file_list_in.append([dir_n, fileN, extN])
        else:
            self.msg_end += "File %s has not a good extension (%s)\n" % (file_name_wo_dir, str(self.auth_ext))
            self.logNB.warning(
                "In  _addFile file %s has not a good extension (%s)" % (file_name_wo_dir, str(self.auth_ext)))

    def getFileList(self):
        """ Create file_list with good path and name.
        It works recursively and use _addFile function
        """
        self.logNB.debug("In  getFileList, arguments=%s" % str(self.arguments))
        if len(self.arguments) != 0:
            for file_or_dir in self.arguments:
                if os.path.isdir(file_or_dir):
                    for dir_path, dir_names, file_names in os.walk(file_or_dir):
                        for file_name in file_names:
                            self._addFile(os.path.join(dir_path, file_name))

                elif os.path.isfile(file_or_dir):
                    self._addFile(file_or_dir)

        self.logNB.info("Out getFileList, file_list=%s" % str(self.file_list_in))

    def getOutFileList(self):
        """ Return the created file list
        """
        return self.file_list_out

    def replace(self, file_name):
        """Function to replace the input file by output file
        """
        pass

    def delete(self):
        """Delete files
        """
        if self.delete_file:
            for (dir_name, file_name, file_ext) in self.file_list_in:
                send2trash.send2trash(os.path.join(dir_name, file_name + file_ext))

    def compute(self):
        """Execute the command for each file and examine the result.
        """
        old_dir = os.getcwd()

        for (dir_name, file_name, file_ext) in self.file_list_in:
            if dir_name != "":
                os.chdir(dir_name)

            # Construct the command
            cmd = self.command.split(" ")
            # input file name
            cmd.append(file_name + file_ext)
            # options
            if self.command_options:
                opts = self.command_options.split(" ")
                cmd += opts
            # output
            if self.command_set_output:
                if file_ext == self.res_ext:
                    # same extension, need to replace the input file with resulted file
                    self.temp_file = os.path.join("/tmp", file_name + self.res_ext)
                    cmd.append(self.temp_file)
                    for com in cmd:
                        # particular case for reducePdfWeight
                        if re.search("output_file_to_replace", com):
                            cmd.remove(com)
                            cmd.remove(self.temp_file)
                            cmd.remove(file_name + file_ext)
                            cmd.append(re.sub("output_file_to_replace", self.temp_file, com))
                            cmd.append(file_name + file_ext)
                else:
                    cmd.append(file_name + self.res_ext)
                    self.file_list_out.append(os.path.join(os.getcwd(), file_name + self.res_ext))
            self.logNB.info("Run command %s" % str(cmd))

            # Execute the command
            process = subprocess.Popen(cmd, stderr=subprocess.STDOUT)
            process.wait()
            if process.returncode != 0:
                # be sure that result file is not well generated (if expected)
                if self.res_ext != "" and not os.path.isfile(file_name + self.res_ext):
                    self.error = True
                    self.msg_end += "In %s,\ncmd failed : \n  %s\n" % (os.getcwd(), str(cmd))
            else:
                if self.temp_file:
                    self.replace(file_name + file_ext)

                else:
                    if self.res_ext != "":
                        self.msg_end += "Executed : %s\n" % (os.path.join(os.getcwd(), file_name + self.res_ext))
                    else:
                        self.msg_end += "Executed : %s\n" % (os.path.join(os.getcwd(), file_name + file_ext))

            # Search for generated files to delete
            for file_to_delete in ("doc_data.txt", self.temp_file):
                if os.path.isfile(file_to_delete):
                    os.remove(file_to_delete)

            if dir_name != "":
                os.chdir(old_dir)

    def runCommand(self, no_windows=False):
        """ Get the file list, if it's not null, execute the command on each file,
        and analyze the result.
        """
        self.getFileList()
        if len(self.file_list_in) != 0:
            self.compute()
        self.analyze(no_windows)

    def analyze(self, no_windows=False):
        """Print a message dialog with the result of the command.
        """
        if len(self.file_list_in) == 0:
            MessageDialogEnd(error=True, log_file=self.log_name, title=self.prog_name, msg1="ERROR",
                             msg2=self.msg_not_found)
            self.logNB.error(self.msg_not_found)
            sys.exit(1)
        elif self.error:
            MessageDialogEnd(error=True, log_file=self.log_name, title=self.prog_name, msg1="ERROR",
                             msg2=self.msg_end)
            self.logNB.error(self.msg_end)
            sys.exit(1)
        else:
            self.delete()
            if not no_windows:
                MessageDialogEnd(error=False, log_file=self.log_name, title=self.prog_name, msg1="OK",
                                 msg2=self.msg_end)
