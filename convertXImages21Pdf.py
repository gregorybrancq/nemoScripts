#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Convert X image files to 1 pdf
"""
import re

from common import createLog, parsingLine
from concatPdf import ConcatPdf
from convertBmp2Jpg import ConvertBmp2Jpg
from convertJpg2Pdf import ConvertJpg2Pdf


def main():
    # Create log class
    root_log = 'convertXImages21Pdf'
    (parsedArgs, args) = parsingLine()
    logger = createLog(root_log, parsedArgs)
    logger.info("START")
    file_list_all_jpg = list()
    for arg in args:
        if re.search(".bmp", arg) or re.search(".BMP", arg):
            # Convert BMP files
            convert_bmp_2_jpg = ConvertBmp2Jpg(root_log, [arg], delete_file=False)
            convert_bmp_2_jpg.run(no_windows=True)
            file_list_all_jpg.append(convert_bmp_2_jpg.getOutFileList()[0])
        else:
            file_list_all_jpg.append(arg)

    #  Convert JPG files to PDF
    convert_all_jpg_2_pdf = ConvertJpg2Pdf(root_log, file_list_all_jpg, delete_file=False)
    convert_all_jpg_2_pdf.run(no_windows=True)

    # Convert in PDF
    file_list_all_pdf = convert_all_jpg_2_pdf.getOutFileList()
    ConcatPdf(root_log, file_list_all_pdf).run()
    logger.info("STOP\n")


if __name__ == '__main__':
    main()
