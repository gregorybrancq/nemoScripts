#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Class for Nemo scripts
"""
import logging

class NemoBase:
    def __init__(self, root_log):
        self.logger = logging.getLogger('.'.join([root_log, __name__]))
        self.logger.info("creating an instance")
        self.extension = list()
        self.file_list = list()
        self.parse_line = str()

    def oo(self):
        self.logger.info("In222 oo")

    def getFileList(self):
        self.logger.info(header, "In  listFromArgs")
        typeList = list()
        warnNb = 0

        if len(args) != 0:
            for arg in args:
                # arg.encode('latin1')
                if os.path.isdir(arg):
                    self.logger.info(header, "In  listFromArgs dir=" + str(arg))
                    for dirpath, dirnames, filenames in os.walk(arg):
                        for filename in filenames:
                            (typeList, warnNb) = addFile(self.logger, header, os.path.join(dirpath, filename), ext,
                                                         typeList,
                                                         warnNb)

                elif os.path.isfile(arg):
                    self.logger.info(header, "In  listFromArgs file=" + str(arg))
                    (typeList, warnNb) = addFile(self.logger, header, arg, ext, typeList, warnNb)

        self.logger.info(header, "Out listFromArgs typeList=" + str(typeList))
        return typeList, warnNb
        (self._file_list, count_warn) = listFromArgs(self.logger, HEADER, args, auth_ext)

    def runJob(self):
        pass

    def analyzeJob(self):
        pass

    # def listFromArgs(log, header, args, ext):
    #    log.info(header, "In  listFromArgs")
    #    typeList = list()
    #    warnNb = 0

    #    if (len(args) != 0):
    #        for arg in args:
    #            # arg.encode('latin1')
    #            if (os.path.isdir(arg)):
    #                log.info(header, "In  listFromArgs dir=" + str(arg))
    #                for dirpath, dirnames, filenames in os.walk(arg):
    #                    for filename in filenames:
    #                        (typeList, warnNb) = addFile(log, header, os.path.join(dirpath, filename), ext, typeList,
    #                                                     warnNb)

    #            elif (os.path.isfile(arg)):
    #                log.info(header, "In  listFromArgs file=" + str(arg))
    #                (typeList, warnNb) = addFile(log, header, arg, ext, typeList, warnNb)

    #    log.info(header, "Out listFromArgs typeList=" + str(typeList))
    #    return typeList, warnNb
