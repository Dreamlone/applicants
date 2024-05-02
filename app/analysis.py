import pandas as pd


def average_number_of_applications_per_person_per_year(df: pd.DataFrame):
    """ Calculate statistics on the dataset """
    df = df[['Year.of.application', 'Applicant.ID', 'Gender']]
    df = df.dropna()

    years = list(df['Year.of.application'].unique())
    years.sort()
    applications_per_person = []
    for year in years:
        year_df = df[df['Year.of.application'] == year]

        year_df = year_df.groupby(['Applicant.ID']).agg({'Gender': 'count'})
        year_df = year_df.reset_index()
        year_df = year_df.rename(columns={'Gender': 'Number of applications'})

        avg = year_df["Number of applications"].mean()
        print(f'{year}: {avg:.2f}')
        applications_per_person.append(avg)

    print(f'Applications per person: {sum(applications_per_person) / len(applications_per_person)}')