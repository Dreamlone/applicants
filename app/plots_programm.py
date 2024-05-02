import shutil
from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

PROGRAM_NAME = {"Bachelor's Programme in Psychology": "BS Psychology",
                "Master's Programme in Pharmacy": "MS Pharmacy",
                "Bachelor's Programme in Logopedics": "BS Logopedics",
                "Bachelor's Programme in Social Research": "BS Social Research",
                "Bachelor's Programme in Law": "BS Law",
                "Bachelor's Programme in Politics, Media and Communication": "BS Politics, Media and Communication",
                "Bachelor's Programme in History": "BS History",
                "Degree Programme in Medicine": "Medicine",
                "Bachelor's Programme in Society and Change": "BS Society and Change",
                "Bachelor's Programme in Philosophy": "BS Philosophy",
                "Bachelor's Programme in Biology": "BS Biology",
                "Master's Programme in Food Economy and Consumption": "BS Food Economy and Consumption",
                "Bachelor's Programme in Art Studies": "BS Art Studies",
                "Bachelor's Programme in Cultural Studies": "BS Cultural Studies",
                "Bachelor's Programme in Molecular Biosciences": "BS Molecular Biosciences",
                "Degree Programme in Dentistry": "Dentistry",
                "Bachelor's Programme in Veterinary Medicine": "BS Veterinary Medicine",
                "Bachelor's Programme in Economics": "BS Economics",
                "Bachelor's Programme in Geography": "BS Geography",
                "Bachelor's Programme in Education": "BS Education",
                "Bachelor's Programme in Enviromental Sciences": "BS Enviromental Sciences",
                "Bachelor's Programme in Pharmacy": "BS Pharmacy",
                "Bachelor's Programme in Languages": "BS Languages",
                "Bachelor's Programme in Food Sciences": "BS Food Sciences",
                "Bachelor's Programme in Chemistry": "BS Chemistry",
                "Bachelor's Programme in Geosciences": "BS Geosciences",
                "Bachelor's Programme in Forest Sciences": "BS Forest Sciences",
                "Bachelor's Programme in Computer Science": "BS Computer Science",
                "Master's Programme in Translation and Interpreting": "MS Translation and Interpreting",
                "Bachelor's Programme in Physical Sciences": "BS Physical Sciences",
                "Bachelor's Programme in the Languages and Literatures of Finland": "BS Languages and Literatures of Finland",
                "Bachelor's Programme in Enviromental and Food Economics": "BS Enviromental and Food Economics",
                "Master's Programme in Finnish and Finno-Ugrian Languages and Cultures": "MS Finnish and Finno-Ugrian Languages and Cultures",
                "Bachelor's Programme in Theology and Religious Studies": "BS Theology and Religious Studies",
                "Bachelor's Programme in Mathematical Sciences": "BS Mathematical Sciences",
                "Bachelorâ€™s program in Social Sciences": "BS Social Sciences",
                "Bachelor's Programme for Teachers of Mathematics, Physics and Chemistry": "BS Teachers of Mathematics, Physics and Chemistry",
                "Bachelor's Programme in Agricultural Sciences": "BS Agricultural Sciences"}


def get_approved_program_data(dataframe: pd.DataFrame):
    dataframe = dataframe[['Year.of.application', 'Applicant.ID', 'Degree.Programme', 'Admission.status']]
    dataframe = dataframe.dropna()
    dataframe = dataframe[dataframe['Admission.status'] == 'APPROVED']
    dataframe = dataframe.drop_duplicates()
    return dataframe


def applications_per_program(df: pd.DataFrame, plot_path: Path):
    approved_per_program = get_approved_program_data(df)

    # Get all programs
    df_pr = df[['Year.of.application', 'Applicant.ID', 'Degree.Programme']]
    df_pr = df_pr.dropna()
    program_df = df_pr.groupby(['Year.of.application', 'Degree.Programme']).agg({'Applicant.ID': 'count'})
    program_df = program_df.reset_index()
    program_df = program_df.sort_values(by=['Degree.Programme', 'Year.of.application'])

    approved_per_program = approved_per_program.groupby(['Year.of.application', 'Degree.Programme']).agg({'Applicant.ID': 'count'})
    approved_per_program = approved_per_program.reset_index()
    approved_per_program = approved_per_program.sort_values(by=['Degree.Programme', 'Year.of.application'])

    program_df['Approved.Applications'] = approved_per_program['Applicant.ID']

    # Calculate competitiveness
    program_df['competitiveness'] = program_df['Approved.Applications'] / program_df['Applicant.ID']
    competitiveness_df = program_df.groupby('Degree.Programme').agg({'competitiveness': 'mean'})
    competitiveness_df = competitiveness_df.reset_index()
    competitiveness_df = competitiveness_df.sort_values(by='competitiveness')
    competitiveness_df['Degree.Programme'] = competitiveness_df['Degree.Programme'].replace(PROGRAM_NAME)

    fig_size = (12.0, 4.0)
    fig, ax = plt.subplots(figsize=fig_size)
    plt.bar(competitiveness_df['Degree.Programme'],
            competitiveness_df['competitiveness'])
    plt.xticks(competitiveness_df['Degree.Programme'],
               competitiveness_df['Degree.Programme'], rotation=90)
    plt.grid()
    plt.xlabel('Program name')
    plt.ylabel('Coefficient of competitiveness')
    plt.savefig(Path(plot_path, f'programs_info.png'),
                dpi=300, bbox_inches='tight')
    plt.close()

