from pathlib import Path

import bamt.networks as networks
import bamt.preprocessors as pp

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

from pgmpy.estimators import K2Score

from app.paths import get_data_path


def apply_bayesian_network():
    columns = ['Year.of.application', 'Faculty', 'Degree.Programme',
               'Priority', 'Year.of.birth', 'First.time.applicant', 'Municipality',
               'Gender', 'Admission.status', 'previous.qualifications', 'First.language']
    df = pd.read_csv(Path(get_data_path(), 'applicant_data.csv'),
                     sep=';', encoding='cp1252', nrows=500)
    df = df[columns]
    df['First.time.applicant'] = df['First.time.applicant'].astype(bool)

    df = df.dropna()
    df['Age'] = df['Year.of.application'] - df['Year.of.birth']
    for col in columns:
        updated = []
        for i in df[col]:
            updated.append(str(i))
        df[col] = updated

    data = df[['Admission.status', 'Age', 'Degree.Programme',
               'previous.qualifications', 'First.language', 'Faculty',
               'First.time.applicant']]
    data['Age'] = data['Age'].astype(float)

    encoder = preprocessing.LabelEncoder()
    discretizer = preprocessing.KBinsDiscretizer(n_bins=5, encode='ordinal', strategy='quantile')

    p = pp.Preprocessor([('encoder', encoder), ('discretizer', discretizer)])
    discretized_data, est = p.apply(data)

    bn = networks.HybridBN(has_logit=True, use_mixture=True)
    info = p.info
    bn.add_nodes(info)
    bn.add_edges(discretized_data, scoring_function=('K2', K2Score))
    bn.set_classifiers(classifiers={'Admission.status': RandomForestClassifier()})
    bn.fit_parameters(data)
    bn.plot('bn.html')


if __name__ == '__main__':
    apply_bayesian_network()
