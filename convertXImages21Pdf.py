#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Convert X image files to 1 pdf
"""
import os
import re

from common import createLog, parsingLine
from concatPdf import ConcatPdf
from convertBmp2Jpg import ConvertBmp2Jpg
from convertJpg2Pdf import ConvertJpg2Pdf
from message import MessageDialogEnd


def main():
    # Create log class
    root_log = 'convertXImages21Pdf'
    (parsedArgs, args) = parsingLine()
    logger = createLog(root_log, parsedArgs)
    logger.info("START")
    logger.info(str(args))
    root_dir = os.getcwd()
    msg_status_global = "PASS"
    msg_end_global = ""
    for arg in sorted(args):
        logger.debug("Enter %s" % str(arg))
        for dirpath, dirnames, filenames in os.walk(arg, topdown=False):  # @UnusedVariable
            if not dirnames and filenames:
                file_list_all_jpg = list()
                os.chdir(dirpath)
                logger.debug("Enter %s" % str(dirpath))
                for filename in filenames:
                    if re.search(".bmp", filename) or re.search(".BMP", filename):
                        # Convert BMP files
                        logger.debug("Bmp files : %s" % str(filename))
                        convert_bmp_2_jpg = ConvertBmp2Jpg(root_log, [filename], delete_file=True)
                        logger.debug("Convert file : %s" % str(filename))
                        convert_bmp_2_jpg.run(no_windows=True)
                        file_list_all_jpg.append(convert_bmp_2_jpg.getOutFileList()[0])
                    else:
                        file_list_all_jpg.append(filename)

                # Sort file list
                file_list_all_jpg_sorted = list()
                for jpg_files in sorted(file_list_all_jpg):
                    file_list_all_jpg_sorted.append(jpg_files)

                # Convert JPG files to PDF
                convert_all_jpg_2_pdf = ConvertJpg2Pdf(root_log, file_list_all_jpg_sorted, delete_file=False)
                convert_all_jpg_2_pdf.run(no_windows=True)

                # Convert in PDF
                file_list_all_pdf = convert_all_jpg_2_pdf.getOutFileList()
                concat_pdf = ConcatPdf(root_log, file_list_all_pdf)
                concat_pdf.run(no_windows=True)

                # Get result
                (log_name, msg_status, msg_end) = concat_pdf.getResult()
                if not msg_end_global:
                    msg_end_global = msg_end
                else:
                    msg_end_global = msg_end_global + "\n" + msg_end
                if msg_status != "PASS":
                    msg_status_global = "ERROR"

            os.chdir(root_dir)

    MessageDialogEnd(error=False, log_file=log_name, title=root_log,
                     msg1=msg_status_global, msg2=msg_end_global)
    logger.info("STOP\n")


if __name__ == '__main__':
    main()
