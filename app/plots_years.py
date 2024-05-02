from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def applications_per_year_by_gender(df: pd.DataFrame, plot_path: Path):
    """ Generate general plot with distribution per year with applications per gender """

    df = df[['Year.of.application', 'Applicant.ID', 'Gender']]
    df = df.dropna()
    year_df = df.groupby('Year.of.application').agg({'Applicant.ID': 'count'})
    year_df = year_df.reset_index()
    year_df = year_df.sort_values(by='Year.of.application')

    applications_per_gender = df.groupby(['Year.of.application', 'Gender']).agg({'Applicant.ID': 'count'})
    applications_per_gender = applications_per_gender.reset_index()
    males = applications_per_gender[applications_per_gender['Gender'] == 'male'].sort_values(by='Year.of.application')
    males['percent'] = (np.array(males['Applicant.ID']) / np.array(year_df['Applicant.ID'])) * 100

    females = applications_per_gender[applications_per_gender['Gender'] == 'female'].sort_values(by='Year.of.application')
    females['percent'] = (np.array(females['Applicant.ID']) / np.array(year_df['Applicant.ID'])) * 100
    females['Applicant.ID'] = np.array(females['Applicant.ID']) + np.array(males['Applicant.ID'])

    fig_size = (10.0, 4.0)
    fig, ax = plt.subplots(figsize=fig_size)

    plt.plot(year_df['Year.of.application'], year_df['Applicant.ID'], '-ok',
             c='black', alpha=1.0)
    plt.fill_between(males['Year.of.application'], [0] * len(males), males['Applicant.ID'],
                     alpha=.2, linewidth=0, color='blue', label='sent by males')
    plt.fill_between(females['Year.of.application'], males['Applicant.ID'], females['Applicant.ID'],
                     alpha=.2, linewidth=0, color='orange', label='sent by females')
    for i, row in females.iterrows():
        y_loc = row['Applicant.ID'] - 5000
        ax.text(row['Year.of.application'] - 0.1, y_loc, f"{row['percent']:.0f}%", fontsize=12, c='orange')
    for i, row in males.iterrows():
        y_loc = row['Applicant.ID'] - 5000
        ax.text(row['Year.of.application'] - 0.1, y_loc, f"{row['percent']:.0f}%", fontsize=12, c='blue')

    plt.grid()
    plt.xlabel('Year')
    plt.ylabel('Number of applications')
    plt.title('Applications number analysis (by gender)')
    plt.legend()
    plt.savefig(Path(plot_path, f'applications_number_gender.png'), dpi=300, bbox_inches='tight')
    plt.close()


def accepted_applications_per_year_by_gender(df: pd.DataFrame, plot_path: Path):
    """ Generate general plot with distribution per """

    df = df[['Year.of.application', 'Applicant.ID', 'Gender', 'Admission.status']]
    df = df.dropna()
    df = df[df['Admission.status'] == 'APPROVED']
    df = df.drop_duplicates()
    year_df = df.groupby('Year.of.application').agg({'Applicant.ID': 'count'})
    year_df = year_df.reset_index()
    year_df = year_df.sort_values(by='Year.of.application')

    applications_per_gender = df.groupby(['Year.of.application', 'Gender']).agg({'Applicant.ID': 'count'})
    applications_per_gender = applications_per_gender.reset_index()
    males = applications_per_gender[applications_per_gender['Gender'] == 'male'].sort_values(by='Year.of.application')
    males['percent'] = (np.array(males['Applicant.ID']) / np.array(year_df['Applicant.ID'])) * 100

    females = applications_per_gender[applications_per_gender['Gender'] == 'female'].sort_values(by='Year.of.application')
    females['percent'] = (np.array(females['Applicant.ID']) / np.array(year_df['Applicant.ID'])) * 100
    females['Applicant.ID'] = np.array(females['Applicant.ID']) + np.array(males['Applicant.ID'])

    fig_size = (10.0, 4.0)
    fig, ax = plt.subplots(figsize=fig_size)

    plt.plot(year_df['Year.of.application'], year_df['Applicant.ID'], '-ok',
             c='grey', alpha=1.0)
    plt.fill_between(males['Year.of.application'], [0] * len(males), males['Applicant.ID'],
                     alpha=.2, linewidth=0, color='blue', label='males')
    plt.fill_between(females['Year.of.application'], males['Applicant.ID'], females['Applicant.ID'],
                     alpha=.2, linewidth=0, color='orange', label='females')
    for i, row in females.iterrows():
        y_loc = row['Applicant.ID'] - 300
        ax.text(row['Year.of.application'] - 0.1, y_loc, f"{row['percent']:.0f}%", fontsize=12, c='orange')
    for i, row in males.iterrows():
        y_loc = row['Applicant.ID'] - 300
        ax.text(row['Year.of.application'] - 0.1, y_loc, f"{row['percent']:.0f}%", fontsize=12, c='blue')

    plt.grid()
    plt.xlabel('Year')
    plt.ylabel('Number of applicants')
    plt.title('Approved applications number analysis (by gender)')
    plt.legend()
    plt.savefig(Path(plot_path, f'accepted_applications_number_gender.png'), dpi=300, bbox_inches='tight')
    plt.close()
