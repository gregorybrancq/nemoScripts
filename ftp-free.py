#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Convert bmp to jpg
"""

# Import
import logging

from common import createLog, parsingLine
from nemoBase import NemoBase


class SendByFtpFree(NemoBase):
    def __init__(self, root_log, args):
        root_log_name = '.'.join([root_log, self.__class__.__name__])
        self.logCB = logging.getLogger(root_log_name)
        super().__init__(root_log, root_log_name, args)

    def run(self):
        command = "ftp-free-shell"
        command_param = False
        delete_file = True
        auth_ext = []
        res_ext = ""
        msg_not_found = "No file has been found."
        self.setConfig(command, command_param, delete_file, auth_ext, res_ext, msg_not_found)
        self.runCommand()


def main():
    # Create log class
    root_log = 'ftp-free'
    (parsedArgs, args) = parsingLine()
    logger = createLog(root_log, parsedArgs)
    logger.info("START")
    SendByFtpFree(root_log, args).run()
    logger.info("STOP")


if __name__ == '__main__':
    main()

    ## Print result
    #msg = "Fichier envoyé : " + str(fileN) + "\n\n"
    #if re.search("Fichier d'origine :", out) :
    #    msg += "URL de download: " + "\n"
    #    msg += "    " + re.findall("URL Fichier depose : (.*)", out)[0] + "\n"
    #if re.search("URL pour suppression du fichier :", out) :
    #    msg += "URL de suppression: " + "\n"
    #    msg += "    " + re.sub("&", "&amp;", re.findall("URL pour suppression du fichier : (.*)", out)[0]) + "\n"
