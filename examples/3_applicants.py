from pathlib import Path

import pandas as pd

from app.paths import get_data_path, eda_results_folder
from app.plots_faculties import applications_per_faculties

import warnings

warnings.filterwarnings('ignore')


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


def explore_applicants():
    """ Show some patterns related to applicanta """
    df = pd.read_csv(Path(get_data_path(), 'applicant_data.csv'),
                     sep=';', encoding='ISO-8859-1')

    plot_path = eda_results_folder('applicants')

    df = df[['Applicant.ID', 'Year.of.application', 'Faculty', 'Degree.Programme',
             'Priority', 'Year.of.birth', 'First.time.applicant', 'Municipality',
             'Gender', 'Admission.status', 'previous.qualifications']]
    df = df.dropna()
    df['Degree.Programme'] = df['Degree.Programme'].replace(PROGRAM_NAME)

    for program in list(df['Degree.Programme'].unique()):
        df_program = df[df['Degree.Programme'] == program]

        df_program


if __name__ == '__main__':
    explore_applicants()
