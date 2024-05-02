from pathlib import Path

import pandas as pd

from app.analysis import average_number_of_applications_per_person_per_year
from app.description import describe_table
from app.paths import get_data_path, eda_results_folder
from app.plots_years import applications_per_year_by_gender, \
    accepted_applications_per_year_by_gender

import warnings
warnings.filterwarnings('ignore')


def read_file_and_explore():
    """ Code to explore provided data """
    df = pd.read_csv(Path(get_data_path(), 'applicant_data.csv'),
                     sep=';', encoding='cp1252')

    describe_table(df)

    # Generate folder for plots
    plot_path = eda_results_folder('years_and_gender')

    # Move step by step - first plots with datetime changes
    applications_per_year_by_gender(df, plot_path)
    accepted_applications_per_year_by_gender(df, plot_path)

    # Statistics calculation
    average_number_of_applications_per_person_per_year(df)


if __name__ == '__main__':
    read_file_and_explore()
