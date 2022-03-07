import os
import shutil
import pandas
from filter import Filter


def test_validate_file_not_exists_raise_exception():
    filter = Filter('non-existing.csv')

    try:
        filter.validate_file_exists()
        validated = False
    except Exception as excepttion:
        validated = isinstance(excepttion, FileNotFoundError)

    assert validated


def test_validate_file_exists():
    filter = Filter('samples/pcm_donaciones_sample.csv')

    try:
        filter.validate_file_exists()
        validated = True
    except Exception as excepttion:
        validated = False

    assert validated


def test_read_file():
    filter = Filter('samples/pcm_donaciones_sample.csv')

    filter.read_file()

    assert isinstance(filter.data_frame, pandas.DataFrame)


def test_split_regions_in_files():
    filter = Filter('samples/pcm_donaciones_sample.csv', True)
    filter.output_path = filter.output_path.replace('regions', 'regions_test')
    filter.read_file()

    filter.split_regions_in_files()

    assert os.path.isdir(filter.output_path)

    regions = ['piura.csv', 'cusco.csv', 'lima.csv']

    for i, region in enumerate(regions):
        filepath = os.path.join(filter.output_path, region)
        assert os.path.exists(filepath)

        assert len(pandas.read_csv(filepath).index) == i+1

    shutil.rmtree(filter.output_path)


def test_parse():
    filter = Filter('samples/pcm_donaciones_sample.csv', True)
    filter.output_path = filter.output_path.replace('regions', 'regions_test')

    assert filter.parse()

    shutil.rmtree(filter.output_path)
