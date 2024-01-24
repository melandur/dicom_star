import os
import sys

from loguru import logger

from dicom_star.core.analyzer import DicomAnalyzer

logger.remove()  # removes default logger
logger.add(sys.stderr, level='INFO')  # TRACE, DEBUG, INFO, WARNING, ERROR


if __name__ == '__main__':
    src_folder = ''

    folders = sorted(os.listdir(src_folder))
    folders = [folder for folder in folders if os.path.isdir(os.path.join(src_folder, folder))]

    for folder in folders:
        files = sorted(os.listdir(os.path.join(src_folder, folder)))

        if len([file for file in files if file.endswith('.DICOM') or file.endswith('.dcm')]) >= 1:
            src_file = os.path.join(src_folder, folder, [file for file in files if file.endswith('.dcm')][0])

            da = DicomAnalyzer(src_file)
            print(da)
            results = da.get_sequence()

            print(results, os.path.basename(src_file))
