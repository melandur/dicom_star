import copy
import json
import os

import pydicom
import toml
from loguru import logger

from dicom_star.core.logic import DicomFilter, ValueFilter
from dicom_star.core.tokens import create_filter_logic, tokenize_filter_string


class DicomAnalyzer:
    def __init__(self, src: str) -> None:
        self.src = src
        self.definitions = None
        self.dicom_tags = None

        self._load_definitions()
        self._read_dicom_tags()

    def __str__(self):
        """Returns a string representation with only the tags of interest"""

        tags_of_interest = [
            '00080060',  # Modality
            '00080008',  # Image Type
            '0008103E',  # Series Description
            '00180081',  # Echo Time
            '00180024',  # Sequence Name
            '00180080',  # Repetition Time
        ]  # only for fast printing, can be extended with user specific tags

        filtered_tags = {k: v for k, v in self.dicom_tags.items() if k in tags_of_interest}
        return f'{json.dumps(filtered_tags, indent=4)}'

    def _load_definitions(self) -> None:
        """Reads the definitions.toml file and stores the content in self.definitions"""

        definitions_file = os.path.join(os.getcwd(), 'definitions.toml')
        if not os.path.exists(definitions_file):
            raise FileNotFoundError('definitions.toml not found')

        with open(definitions_file, 'r') as f:
            definitions = toml.load(f)
        self.definitions = definitions

    def _read_dicom_tags(self) -> None:
        if not os.path.isfile(self.src):
            raise FileNotFoundError(f'File not found: {self.src}')

        self.dicom_tags = {}

        ds = pydicom.dcmread(self.src)
        dicom_tags = ds.to_json_dict()
        tmp_dicom_tags = copy.deepcopy(dicom_tags)

        for id in tmp_dicom_tags:
            if ds[id].VR in ('OB', 'OW', 'UN'):  # ignore binary data and unknown tags
                del dicom_tags[id]
                continue

            if ds[id].value:  # lower case value key and remove tag ids with empty values
                dicom_tags[id]['value'] = dicom_tags[id]['Value']
                del dicom_tags[id]['Value']
            else:
                del dicom_tags[id]
                continue

            del dicom_tags[id]['vr']
            dicom_tags[id]['keyword'] = ds[id].keyword
            dicom_tags[id]['name'] = ds[id].name

        self.dicom_tags = dicom_tags

    def get_sequence(self) -> dict:
        """Returns a dict with the results of the sequence definitions sorted by match ratio"""

        results = {}
        for sequence_name, definitions in self.definitions.items():
            results[sequence_name] = {}
            results[sequence_name]['total_tags'] = len(definitions.keys())
            results[sequence_name]['found_tags'] = 0
            results[sequence_name]['match_ratio'] = 0.0
            results[sequence_name]['found_tag_ids'] = []

            for tag, definition in definitions.items():
                tokens = tokenize_filter_string(definition)
                filter_statement = create_filter_logic(tokens, 'ValueFilter')

                tag_data = self.dicom_tags.get(tag)
                if tag_data is None:
                    logger.warning(f'Tag {tag} not found in {self.src}')
                    continue

                dicom_filter = DicomFilter()
                if dicom_filter.filter(tag_data, eval(filter_statement)):
                    results[sequence_name]['found_tags'] += 1
                    ratio = results[sequence_name]['found_tags'] / results[sequence_name]['total_tags']
                    results[sequence_name]['match_ratio'] = ratio
                    results[sequence_name]['found_tag_ids'].append(tag)

        # sort results by found_tags_ratio
        results = {k: v for k, v in sorted(results.items(), key=lambda item: item[1]['match_ratio'], reverse=True)}
        results = {k: f'{v["match_ratio"]:.2f}' for k, v in results.items()}
        return results
