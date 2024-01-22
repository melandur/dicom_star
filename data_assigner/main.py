import os
import sys

from loguru import logger

logger.remove()
logger.add(sys.stderr, level='ERROR')

from data_assigner.analyzer import DicomAnalyzer

if __name__ == '__main__':
    sequence_definitions = {
        'T1w': {
            # '00080060': 'MR',  # Modality
            # '00080008': 'T1',  # Image Type
            '0008103E': 'T1 Pre',  # Series Description
            # '00180081': '4.0',  # Echo Time
            # '00180080': '8.6',  # Repetition Time
        },
        'T1c': {
            # '00080060': 'MR',  # Modality
            # '00080008': 'ORIGINAL & PRIMARY & T1',  # Image Type
            '0008103E': 'T1 Post',  # Series Description
            # '00180081': '4.0',  # Echo Time
        },
        'T2w': {
            # '00080060': 'MR',  # Modality
            # '00080008': 'ORIGINAL & PRIMARY & T2',  # Image Type
            '0008103E': 'T2',  # Series Description
            # '00180081': '4.0',  # Echo Time
            # '00180080': '8.6',  # Repetition Time
        },
        'FLAIR': {
            # '00080060': 'MR',  # Modality
            # '00080008': 'ORIGINAL & PRIMARY & FLAIR',  # Image Type
            '0008103E': 'Flair',  # Series Description
            # '00180081': '4.0',  # Echo Time
            # '00180080': '8.6',  # Repetition Time
        },
        # 'DWI': {
        #     '00080060': 'MR',  # Modality
        #     '00080008': 'DERIVED & SECONDARY & DWI',  # Image Type
        #     '00180081': '4.0',  # Echo Time
        #     '00180080': '8.6',  # Repetition Time
        # },
        # 'ADC': {
        #     '00080060': 'MR',  # Modality
        #     '00080008': 'DERIVED & SECONDARY & ADC',  # Image Type
        #     '00180081': '4.0',  # Echo Time
        #     '00180080': '8.6',  # Repetition Time
        # },
        # 'T2-Star': {
        #     '00080060': 'MR',  # Modality
        #     '00080008': 'ORIGINAL & PRIMARY & T2*',  # Image Type
        #     '00180081': '4.0',  # Echo Time
        #     '00180080': '8.6',  # Repetition Time
        # },
        # 'PWI': {
        #     '00080060': 'MR',  # Modality
        #     '00080008': 'ORIGINAL & PRIMARY & PERFUSION',  # Image Type
        #     '00180081': '4.0',  # Echo Time
        #     '00180080': '8.6',  # Repetition Time
        # },
        # 'localizer': {
        #     '00080060': 'MR',  # Modality
        #     '00080070': 'SIEMENS',  # Manufacturer
        #     '0008103E': 'localizer',  # Institution Name
        #     '00180020': 'GR',  # Scanning Sequence
        #     '00180021': 'SP & OSP',  # Sequence Variant
        #     '00180023': '2D',  # MR Acquisition Type
        #     '00180024': 'fl2d1 & ~tra',  # Sequence Name
        #     '00180025': 'N',  # Angio Flag
        #     '00180050': '7',  # Slice Thickness
        #     '00180080': '8.6',  # Repetition Time
        #     '00180081': '4.0',  # Echo Time
        #     '00180084': '123',  # Imaging Frequency
        #     '00180087': '3.0',  # Magnetic Field Strength
        #     '00180088': '8.4',  # Spacing Between Slices
        #     '00181030': 'localizer',  # Protocol Name
        #
        # }
    }

    src_folder = ''

    folders = sorted(os.listdir(src_folder))
    folders = [folder for folder in folders if os.path.isdir(os.path.join(src_folder, folder))]

    for folder in folders:
        files = sorted(os.listdir(os.path.join(src_folder, folder)))

        if len([file for file in files if file.endswith('.DICOM') or file.endswith('.dcm')]) >= 1:
            src_file = os.path.join(src_folder, folder, [file for file in files if file.endswith('.dcm')][0])

            da = DicomAnalyzer(src_file, sequence_definitions)
            print(da)
            results = da.get_sequence()

            print(results, os.path.basename(src_file))
