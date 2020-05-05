#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Convert X bmp to 1 pdf
"""

from common import createLog, parsingLine
from concatPdf import ConcatPdf
from convertBmp2Jpg import ConvertBmp2Jpg
from convertJpg2Pdf import ConvertJpg2Pdf


def main():
    # Create log class
    root_log = 'convertXBmp21Pdf'
    (parsedArgs, args) = parsingLine()
    logger = createLog(root_log, parsedArgs)
    logger.info("START")
    convert_all_bmp_2_jpg = ConvertBmp2Jpg(root_log, args)
    convert_all_bmp_2_jpg.run(no_windows=True)
    file_list_all_jpg = convert_all_bmp_2_jpg.getOutFileList()
    convert_all_jpg_2_pdf = ConvertJpg2Pdf(root_log, file_list_all_jpg)
    convert_all_jpg_2_pdf.run(no_windows=True)
    file_list_all_pdf = convert_all_jpg_2_pdf.getOutFileList()
    ConcatPdf(root_log, file_list_all_pdf).run()
    logger.info("STOP")


if __name__ == '__main__':
    main()
