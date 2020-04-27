#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Class for Nemo scripts
"""
import os
import re
import subprocess
import sys
from optparse import OptionParser

import logging


# sys.path.append('/home/greg/Greg/work/env/pythonCommon')
# from message import MessageDialogEnd
# from basic import getLogDir


class NemoBase:
    def __init__(self, root_log, auth_ext, res_ext):
        self.logNB = logging.getLogger('.'.join([root_log, __name__]))
        self.logNB.info("creating an instance")
        self.auth_ext = auth_ext
        self.res_ext = res_ext
        self.warning = 0
        self.file_list = list()
        self.parse_line = str()

    def parsingLine(self):
        parser = OptionParser()
        parser.add_option(
            "-d",
            "--debug",
            action="store_true",
            dest="debug",
            default=False,
            help="Display all debug information"
        )
        (parsedArgs, self.arguments) = parser.parse_args()

    def addFile(self, file_name):
        self.logNB.info("In  addFile file_name=" + str(file_name))
        dir_n = os.path.dirname(file_name)
        dir_n1 = dir_n.replace('(', '\(')
        dir_n2 = dir_n1.replace(')', '\)')
        file_name_wo_dir = re.sub(dir_n2 + "\/", '', file_name)
        (fileN, extN) = os.path.splitext(file_name_wo_dir)
        if self.auth_ext.__contains__(extN):
            self.logNB.info("In  addFile dir_n=" + str(dir_n) + ", fileN=" + str(fileN) + ", extN=" + str(extN))
            self.file_list.append([dir_n, fileN, extN])
        else:
            self.warning += 1
            self.logNB.debug(
                "In  addFile file " + str(file_name_wo_dir) + " is not a good extension as " + str(self.auth_ext))

    def getFileList(self):
        self.logNB.debug("In  getFileList, arguments=%s" % str(self.arguments))
        if len(self.arguments) != 0:
            for file_or_dir in self.arguments:
                if os.path.isdir(file_or_dir):
                    self.logNB.debug("In  getFileList dir=" + str(file_or_dir))
                    for dir_path, dir_names, file_names in os.walk(file_or_dir):
                        for file_name in file_names:
                            self.addFile(os.path.join(dir_path, file_name))

                elif os.path.isfile(file_or_dir):
                    self.logNB.debug("In  getFileList file=" + str(file_or_dir))
                    self.addFile(file_or_dir)

        self.logNB.info("Out getFileList, file_list=" + str(self.file_list))

    def checkFileList(self, msg):
        if len(self.file_list) == 0:
            self.logNB.error(msg)
            sys.exit(1)

    def convert(self):
        self.logNB.info("In  convert")
        old_dir = os.getcwd()

        for (dir_name, file_name, file_ext) in self.file_list:
            self.logNB.info("In  runJob directory " + str(dir_name) + "  runJob " + file_name + file_ext)

            if dir_name != "":
                os.chdir(dir_name)

            cmd = 'convert "' + file_name + file_ext + '" "' + file_name + self.res_ext + '"'
            self.logNB.info("In  runJob cmd=" + str(cmd))
            proc = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT)
            proc.wait()
            if proc.returncode != 0:
                count_error += 1
                self.logNB.error("In  runJob file: issue with " + str(os.path.join(dir_name, file_name + file_ext)))

            if dir_name != "":
                os.chdir(old_dir)

    def analyzeJob(self):
        pass

    def run(self):
        self.logNB.info("In  run")
        self.parsingLine()
        self.getFileList()
        self.checkFileList("No image has been found.")
        self.convert()
        # self.runJob()
        self.analyzeJob()
        # (file_list, count_warn) = listFromArgs(log, HEADER, args, auth_ext)

    ## End dialog
    # MessageDialogEnd(count_warn, count_error, logFile, "Convert images", "\nJob fini.")
