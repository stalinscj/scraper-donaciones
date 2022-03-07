import os
import csv
import pandas
import argparse


class Filter(object):
    """
    Filter object that is composed of the filename to filter
    To initialize:
    :param filename: name of file to filter
    :param quiet: Do not output any message

    USAGE:
        >>> filter = Filter(filename='pcm_donaciones.csv')
        >>> filter.filter()
    """
    def __init__(self, filename: str, quiet: bool = False):
        self.filename = filename
        self.output_path = os.path.join(os.getcwd(), 'regions')
        self.quiet = quiet

    def validate_file_exists(self) -> bool:
        if not os.path.exists(self.filename):
            raise FileNotFoundError(self.filename)

        return True

    def read_file(self):
        self.data_frame = pandas.read_csv(
            self.filename, encoding='latin-1', dtype=str
        )

    def split_regions_in_files(self) -> bool:
        regions = self.data_frame['REGION'].unique()

        os.makedirs(self.output_path, exist_ok=True)

        for region in regions:
            region_data = self.data_frame[self.data_frame.REGION == region]
            filepath = os.path.join(self.output_path, f'{region}.csv'.lower())
            region_data.to_csv(filepath, index=False, quoting=csv.QUOTE_ALL)

            if not self.quiet:
                print(f'{filepath} filtered ok...')

        return True if regions.size else False

    def parse(self) -> bool:
        self.validate_file_exists()

        self.read_file()

        success = self.split_regions_in_files()

        return success

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Filtra los datos por región')
    parser.add_argument('filename', type=str, help='Nombre del archivo')
    parser.add_argument('-q', '--quiet', action='store_true', required=False)

    args = parser.parse_args()

    filter = Filter(filename=args.filename, quiet=args.quiet)
    success = filter.parse()

    if not args.quiet:
        msg = 'Filtrado exitoso' if success else 'No se pudo filtrar los datos'

        print(msg)
