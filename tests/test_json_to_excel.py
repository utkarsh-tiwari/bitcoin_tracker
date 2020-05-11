import sys
import os
import pytest
import pandas as pd
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json_to_excel.json_to_excel as  source_code


def test_create_sample_json():
    count=1
    test_json = source_code.create_sample_json(count=count)
    assert isinstance(test_json, list)
    assert test_json[0]['Ref'] == f'ABC_{count}'
    assert test_json[0]['sample'] == f'sample_status_{count}'


def test_create_sample_json_error():
    test_json = source_code.create_sample_json(count='1')
    assert test_json == "Exception occured!"
    with pytest.raises(Exception):
        test_json = source_code.create_sample_json(count=1)
        assert test_json[1]['Ref'] == f'ABC_{1}'


def test_read_from_excel():
    test_obj = source_code.ExcelHandling()
    assert test_obj.read_from_excel()


def test_write_to_excel():
    DUMMY_JSON_LOAD = [{'Ref': 'test_1', 'sample': 'test_1'}]
    process_file = r"C:\Users\JP\OneDrive\Documents\GitHub\json_to_excel\json_to_excel\processing\excel_database.xlsx"
    test_obj = source_code.ExcelHandling(json_load=DUMMY_JSON_LOAD)
    test_obj.read_from_excel(process_file=process_file)
    assert test_obj.write_to_excel()
    data_ = pd.read_excel(process_file, sheet_name='Sheet1')
    assert data_.values[0][1] == 'test_1'
    assert data_.values[0][2] == 'test_1'
