import shutil
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import contextlib
from PIL import Image

NAMES = {'Faculty of Agriculture and Forestry': 'Agriculture and Forestry',
         'Faculty of Arts': 'Arts',
         'Faculty of Biological and Environmental Sciences': 'Biological and Environmental Sciences',
         'Faculty of Educational Sciences': 'Educational Sciences',
         'Faculty of Law': 'Law',
         'Faculty of Medicine': 'Medicine',
         'Faculty of Pharmacy': 'Pharmacy',
         'Faculty of Science': 'Science',
         'Faculty of Social Sciences': 'Social Sciences',
         'Faculty of Theology': 'Theology',
         'Faculty of Veterinary Medicine': 'Veterinary Medicine',
         'Swedish School of Political Science': 'School of Political Science'}

LABELS = ['Agriculture and Forestry', 'Arts', 'Biological and Environmental Sciences',
          'Educational Sciences', 'Law', 'Medicine', 'Pharmacy', 'Science',
          'Social Sciences', 'Theology', 'Veterinary Medicine', 'School of Political Science']


def get_approved_data(dataframe: pd.DataFrame):
    dataframe = dataframe[['Year.of.application', 'Applicant.ID', 'Faculty', 'Admission.status']]
    dataframe = dataframe.dropna()
    dataframe = dataframe[dataframe['Admission.status'] == 'APPROVED']
    dataframe = dataframe.drop_duplicates()
    return dataframe


def applications_per_faculties(df: pd.DataFrame, plot_path: Path):
    """ Generate general plot with distribution per year with applications per gender """
    tmp_folder_with_plots = Path(plot_path, 'tmp')
    tmp_folder_with_plots.mkdir(parents=True, exist_ok=True)

    approved_df = get_approved_data(df)
    faculty_approved_df = approved_df.groupby(['Year.of.application', 'Faculty']).agg({'Applicant.ID': 'count'})
    faculty_approved_df = faculty_approved_df.reset_index()
    faculty_approved_df = faculty_approved_df.sort_values(by=['Faculty', 'Year.of.application'])

    df = df[['Year.of.application', 'Applicant.ID', 'Faculty']]
    df = df.dropna()
    faculty_df = df.groupby(['Year.of.application', 'Faculty']).agg({'Applicant.ID': 'count'})
    faculty_df = faculty_df.reset_index()
    faculty_df = faculty_df.sort_values(by=['Faculty', 'Year.of.application'])

    # Set some
    cmap = plt.colormaps["tab20c"]
    inner_colors = cmap([1, 3, 5, 7, 9, 11, 13, 15, 17, 20])

    # Generate the pie plot for each year
    years = list(faculty_df['Year.of.application'].unique())
    years.sort()
    LABELS.sort()
    for year in years:
        year_faculty_approved_df = faculty_approved_df[faculty_approved_df['Year.of.application'] == year]
        all_approved_applications = year_faculty_approved_df['Applicant.ID'].sum()
        year_faculty_approved_df['ratio'] = (np.array(year_faculty_approved_df['Applicant.ID']) / all_approved_applications) * 100
        year_faculty_approved_df['Faculty'] = year_faculty_approved_df['Faculty'].replace(NAMES)
        year_faculty_approved_df = year_faculty_approved_df.sort_values(by='Faculty')

        year_df = faculty_df[faculty_df['Year.of.application'] == year]
        all_applications = year_df['Applicant.ID'].sum()

        year_df['ratio'] = (np.array(year_df['Applicant.ID']) / all_applications) * 100
        year_df['Faculty'] = year_df['Faculty'].replace(NAMES)
        year_df = year_df.sort_values(by='Faculty')

        fig_size = (15.0, 6.0)
        fig, axs = plt.subplots(1, 2, figsize=fig_size)
        plt.suptitle(f'{year}', fontsize=20)

        axs[0].pie(np.array(year_df['ratio']), labels=LABELS,
                   autopct='%1.0f%%', colors=inner_colors,
                   textprops={'color': '#353535', 'fontsize': 7}, startangle=45)
        axs[0].set_title(f'Number of applications per faculty')

        axs[1].pie(np.array(year_faculty_approved_df['ratio']),
                   labels=LABELS,
                   autopct='%1.0f%%', colors=inner_colors,
                   textprops={'color': '#353535', 'fontsize': 7}, startangle=40)
        axs[1].set_title(f'Number of positions (approved applications) per faculty')

        plt.savefig(Path(tmp_folder_with_plots, f'{year}_faculties.png'),
                    dpi=300, bbox_inches='tight')
        plt.close()

        if year in [2015, 2022]:
            # Show some statistics
            print(f'Statistics for the year {year}')
            year_df = year_df.sort_values(by='Applicant.ID')
            year_df = year_df.tail(3)

            print(year_df)

    # Generate gif
    files_to_stack = list(tmp_folder_with_plots.iterdir())
    files_to_stack.sort()
    with contextlib.ExitStack() as stack:
        images = (stack.enter_context(Image.open(f)) for f in files_to_stack)
        img = next(images)
        img.save(fp=Path(plot_path, 'faculties.gif'), format='GIF',
                 append_images=images,
                 save_all=True, duration=1200, loop=0)

    shutil.rmtree(tmp_folder_with_plots)
