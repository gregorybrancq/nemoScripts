#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Class for Nemo scripts
"""
import os
import re
import subprocess
import sys

import logging

sys.path.append('/home/greg/Greg/work/env/pythonCommon')
from basic import getLogDir
from message import MessageDialogEnd


class NemoBase:
    def __init__(self, log_name, root_log, arguments, auth_ext, res_ext, msg_not_found):
        self.logNB = logging.getLogger('.'.join([root_log, __name__]))
        self.prog_name = log_name
        self.log_name = os.path.join(getLogDir(), log_name) + ".log"
        self.arguments = arguments
        self.auth_ext = auth_ext
        self.res_ext = res_ext
        self.msg_not_found = msg_not_found
        self.file_list = list()
        self.msg_end = ""
        self.error = False

    def addFile(self, file_name):
        self.logNB.debug("In  addFile file_name=" + str(file_name))
        dir_n = os.path.dirname(file_name)
        dir_n1 = dir_n.replace('(', '\(')
        dir_n2 = dir_n1.replace(')', '\)')
        file_name_wo_dir = re.sub(dir_n2 + "\/", '', file_name)
        (fileN, extN) = os.path.splitext(file_name_wo_dir)
        if self.auth_ext.__contains__(extN):
            self.logNB.debug("In  addFile dir_n=" + str(dir_n) + ", fileN=" + str(fileN) + ", extN=" + str(extN))
            self.file_list.append([dir_n, fileN, extN])
        else:
            self.msg_end += "File %s has not a good extension (%s)\n" % (file_name_wo_dir, str(self.auth_ext))
            self.logNB.warning(
                "In  addFile file %s has not a good extension (%s)" % (file_name_wo_dir, str(self.auth_ext)))

    def getFileList(self):
        self.logNB.debug("In  getFileList, arguments=%s" % str(self.arguments))
        if len(self.arguments) != 0:
            for file_or_dir in self.arguments:
                if os.path.isdir(file_or_dir):
                    self.logNB.debug("In  getFileList, dir=%s" % str(file_or_dir))
                    for dir_path, dir_names, file_names in os.walk(file_or_dir):
                        for file_name in file_names:
                            self.addFile(os.path.join(dir_path, file_name))

                elif os.path.isfile(file_or_dir):
                    self.logNB.debug("In  getFileList file=" + str(file_or_dir))
                    self.addFile(file_or_dir)

        self.logNB.info("file_list=%s" % str(self.file_list))

    def convert(self):
        old_dir = os.getcwd()

        for (dir_name, file_name, file_ext) in self.file_list:
            if dir_name != "":
                os.chdir(dir_name)

            cmd = ['convert', file_name + file_ext, file_name + self.res_ext]
            self.logNB.info("Run command %s" % str(cmd))
            process = subprocess.Popen(cmd, stderr=subprocess.STDOUT)
            process.wait()
            if process.returncode != 0:
                self.error = True
                self.msg_end += "In %s, cmd failed : %s\n" % (os.getcwd(), str(cmd))
            else:
                self.msg_end += "Converted : %s\n" % (os.path.join(os.getcwd(), file_name + self.res_ext))

            if dir_name != "":
                os.chdir(old_dir)

    def analyze(self):
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

    def run(self):
        self.getFileList()
        if len(self.file_list) != 0:
            self.convert()
        self.analyze()
        # self.runJob()
