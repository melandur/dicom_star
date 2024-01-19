import pydicom
import copy
import json

from data_assigner.search_logic import SearchFilter, FileName, FolderNames, Extension

src = '/home/melandur/Downloads/diff_perf_mike/WAS_084_1953-20130327-0/3-ep2d_diff_3scan_p3_m128_ADC/WAS_084_1953_ep2d_diff_3scan_p3_m128_ADC_3_2.dcm'

ds = pydicom.dcmread(src)
data = ds.to_json_dict()
tmp_data = copy.deepcopy(data)

for id in tmp_data:

    if ds[id].VR in ('OB', 'OW'):
        del data[id]
        continue

    data[id]['vm'] = ds[id].VM
    data[id]['keyword'] = ds[id].keyword
    data[id]['name'] = ds[id].name



sf = SearchFilter()

for subject in sf.filter(data,
                         FileName('my_special_name') |
                         FileName('second_special_name') &
                         ~FileName('this_is_bad_data') &
                         FolderNames('my_folder_name', 'sometimes_this_name') &
                         Extension('img', 'jpg')):

    print(f'process -> {subject["file_path"]}')