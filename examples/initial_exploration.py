from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from app.paths import get_data_path, eda_results_folder


def applications_per_year(df: pd.DataFrame, plot_path: Path):
    df = df[['Year.of.application', 'Applicant.ID', 'Gender']]
    df = df.dropna()
    year_df = df.groupby('Year.of.application').agg({'Applicant.ID': 'count'})
    year_df = year_df.reset_index()

    applications_per_gender = df.groupby(['Year.of.application', 'Gender']).agg({'Applicant.ID': 'count'})
    applications_per_gender = applications_per_gender.reset_index()
    males = applications_per_gender[applications_per_gender['Gender'] == 'male'].sort_values(by='Year.of.application')
    females = applications_per_gender[applications_per_gender['Gender'] == 'female'].sort_values(by='Year.of.application')
    females['Applicant.ID'] = np.array(females['Applicant.ID']) + np.array(males['Applicant.ID'])

    fig_size = (10.0, 4.0)
    fig, ax = plt.subplots(figsize=fig_size)

    plt.plot(year_df['Year.of.application'], year_df['Applicant.ID'], '-ok',
             c='black', alpha=1.0)
    plt.fill_between(males['Year.of.application'], [0] * len(males), males['Applicant.ID'],
                     alpha=.2, linewidth=0, color='blue', label='sent by males')
    plt.fill_between(females['Year.of.application'], males['Applicant.ID'], females['Applicant.ID'],
                     alpha=.2, linewidth=0, color='red', label='sent by females')
    plt.grid()
    plt.xlabel('Year')
    plt.ylabel('Number of applications')
    plt.legend()
    plt.savefig(Path(plot_path, f'year.png'), dpi=300, bbox_inches='tight')
    plt.close()


def read_file_and_explore():
    """ Code to explore provided data """
    df = pd.read_csv(Path(get_data_path(), 'applicant_data.csv'),
                     sep=';', encoding='cp1252')

    print(df.size)
    for i in list(df.columns):
        print(f'Column in dataset: {i}')

    # Generate folder for plots
    plot_path = eda_results_folder('initial')

    # Move step by step
    applications_per_year(df, plot_path)


if __name__ == '__main__':
    read_file_and_explore()
