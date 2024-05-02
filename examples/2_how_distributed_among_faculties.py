from pathlib import Path

import pandas as pd

from app.paths import get_data_path, eda_results_folder
from app.plots_faculties import applications_per_faculties

import warnings
warnings.filterwarnings('ignore')


def explore_faculties():
    """ Show some patterns related to faculties """
    df = pd.read_csv(Path(get_data_path(), 'applicant_data.csv'),
                     sep=';', encoding='cp1252')

    plot_path = eda_results_folder('faculties')

    applications_per_faculties(df, plot_path)


if __name__ == '__main__':
    explore_faculties()
