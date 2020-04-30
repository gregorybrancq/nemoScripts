#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Basic functions for file programs as Nemo or Nautilus.
"""
import os
import re
import subprocess
import sys

import logging
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
        :param arguments: arguments pass out to the file program (Nemo or Nautilus
        """
        self.logNB = logging.getLogger('.'.join([root_log, __name__]))
        self.logNB.debug("In init nemoBase")
        self.prog_name = log_name
        self.log_name = os.path.join(getLogDir(), log_name) + ".log"
        self.arguments = arguments
        self.command = str()
        self.command_param = True
        self.delete_file = False
        self.auth_ext = list()
        self.res_ext = str()
        self.msg_not_found = str()
        self.file_list = list()
        self.msg_end = ""
        self.error = False

    def setConfig(self, command, command_param, delete_file, auth_ext, res_ext, msg_not_found):
        """Set the configuration of the class parameters

        :param command: the command to execute
        :param command_param: specify the output file with extension to the command (default False)
        :param delete_file: True to delete the input file (default False)
        :param auth_ext: the authorized extension
        :param res_ext: the file extension result
        :param msg_not_found: if no file matches, it will indicate this message information
        :return: updated attributes
        """
        self.command = command
        self.command_param = command_param
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
        if len(self.auth_ext) == 0 or self.auth_ext.__contains__(extN):
            self.logNB.debug("In  _addFile dir_n=" + str(dir_n) + ", fileN=" + str(fileN) + ", extN=" + str(extN))
            self.file_list.append([dir_n, fileN, extN])
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
                    self.logNB.debug("In  getFileList, dir=%s" % str(file_or_dir))
                    for dir_path, dir_names, file_names in os.walk(file_or_dir):
                        for file_name in file_names:
                            self._addFile(os.path.join(dir_path, file_name))

                elif os.path.isfile(file_or_dir):
                    self.logNB.debug("In  getFileList file=" + str(file_or_dir))
                    self._addFile(file_or_dir)

        self.logNB.info("file_list=%s" % str(self.file_list))

    def compute(self):
        """Execute the command for each file and examine the result.
        """
        old_dir = os.getcwd()

        for (dir_name, file_name, file_ext) in self.file_list:
            if dir_name != "":
                os.chdir(dir_name)

            cmd = self.command.split(" ")
            cmd.append(file_name + file_ext)
            if self.command_param:
                cmd.append(file_name + self.res_ext)
            self.logNB.info("Run command %s" % str(cmd))
            process = subprocess.Popen(cmd, stderr=subprocess.STDOUT)
            process.wait()
            if process.returncode != 0:
                # be sure that result file is not well generated (if expected)
                if self.res_ext != "" and not os.path.isfile(file_name + self.res_ext):
                    self.error = True
                    self.msg_end += "In %s, cmd failed : \n  %s\n" % (os.getcwd(), str(cmd))
            else:
                if self.res_ext != "":
                    self.msg_end += "Executed : %s\n" % (os.path.join(os.getcwd(), file_name + self.res_ext))
                else:
                    self.msg_end += "Executed : %s\n" % (os.path.join(os.getcwd(), file_name + file_ext))
                if self.delete_file:
                    send2trash.send2trash(file_name + file_ext)

            if dir_name != "":
                os.chdir(old_dir)

    def computeProgram(self):
        """Execute the program for the first argument.
        """
        (dir_name, file_name, file_ext) = self.file_list[0]
        cmd = self.command.split(" ")
        cmd.append(os.path.join(dir_name, file_name + file_ext))
        self.logNB.info("Run command %s" % str(cmd))
        process = subprocess.Popen(cmd, stderr=subprocess.STDOUT)
        process.wait()

    def analyze(self):
        """Print a message dialog with the result of the command.
        """
        if len(self.file_list) == 0:
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
            MessageDialogEnd(error=False, log_file=self.log_name, title=self.prog_name, msg1="OK",
                             msg2=self.msg_end)

    def runCommand(self):
        """ Get the file list, if it's not null, execute the command on each file,
        and analyze the result.
        """
        self.getFileList()
        if len(self.file_list) != 0:
            self.compute()
        self.analyze()

    def runProgram(self):
        """ Get the file list, execute the program with the first file in argument.
        """
        self.getFileList()
        if len(self.file_list) != 0:
            self.computeProgram()
        #self.analyze()