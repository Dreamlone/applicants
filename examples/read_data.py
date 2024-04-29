from pathlib import Path

import pandas as pd

from app.paths import get_data_path


def read_file():
    df = pd.read_csv(Path(get_data_path(), 'applicant_data.csv'),
                     sep=';',
                     nrows=10000)
    print(df)


if __name__ == '__main__':
    read_file()
