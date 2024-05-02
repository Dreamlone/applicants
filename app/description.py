import pandas as pd


def describe_table(df: pd.DataFrame):
    """ Display some statistics about dataframe

    :param df: dataframe for analysis
    """

    print(f'Size of the dataset: {len(df)}')
    print(f'Number of columns: {len(list(df.columns))}')
    for i in list(df.columns):
        print(f'Column in dataset: {i}')

    # Show in percentage
    print((df.isna().sum() / len(df)) * 100)

